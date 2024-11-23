import logging
import os
import sys
import time
from multiprocessing import Process

from PIL.ImageQt import QImage
from PySide6.QtCore import QTimer, QObject, QCoreApplication

from core.utilities.helper import parse_directory_into_dictionary, qimage_to_cv2, imgaug_transformation, cv2_to_qimage, \
    transparent_to_hue


# ANSI escape codes for coloring
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_RESET = "\033[0m"


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Color the processName for MainProcess (WorkerManager)
        # if record.processName == "MainProcess":
        #     record.processName = f"{COLOR_GREEN}{record.processName}{COLOR_RESET}"
        # else:
        #     # Color worker process names
        #     record.processName = f"{COLOR_GREEN}{record.processName}{COLOR_RESET}"

        record.processName = f"{COLOR_GREEN}{record.processName}{COLOR_RESET}"
        return super().format(record)


# Configure logging to avoid overlapping output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(processName)s - PID:%(process)d] - %(message)s",
    datefmt="%H:%M:%S",
)

# Apply custom formatter
logger = logging.getLogger()
for handler in logger.handlers:
    handler.setFormatter(CustomFormatter('%(asctime)s - [%(processName)s - PID:%(process)d] - %(message)s', datefmt="%H:%M:%S"))


catalog_path = "coin_catalog"


def split_path(path):
    normalized_path = os.path.normpath(path)
    components = normalized_path.split(os.sep)
    return components


def augment(augmentation_path, cropped_coin_photo_path, uncropped_coin_photo_path):
    uncropped_image = QImage(uncropped_coin_photo_path)
    cropped_image = QImage(cropped_coin_photo_path)
    filename_without_extension = os.path.splitext(os.path.basename(uncropped_coin_photo_path))[0]

    cv2_uncropped_image = qimage_to_cv2(uncropped_image)
    cv2_cropped_image = qimage_to_cv2(cropped_image)

    for i in range(200):
        cv2_augmented_uncropped_image, cv2_augmented_croped_image = (
            imgaug_transformation(full_image=cv2_uncropped_image, hue_image=cv2_cropped_image))

        full_image = cv2_to_qimage(cv2_augmented_uncropped_image)
        cv2_hue_image = transparent_to_hue(cv2_augmented_croped_image)
        croped_image = cv2_to_qimage(cv2_hue_image)

        full_image.save(
            os.path.join(f"{os.path.join(augmentation_path, filename_without_extension)}_{i}_full.png"))
        croped_image.save(
            os.path.join(f"{os.path.join(augmentation_path, filename_without_extension)}_{i}_hue.png"))


def get_augmentation_tasks():
    out = []
    catalog_dict = parse_directory_into_dictionary(catalog_path)
    os.makedirs(os.path.join(catalog_path, "augmented"), exist_ok=True)

    for country in catalog_dict.keys():
        for coin_name in catalog_dict[country].keys():
            for year in catalog_dict[country][coin_name].keys():
                os.makedirs(os.path.join(catalog_path, country, coin_name, year), exist_ok=True)

                for coin_photo in catalog_dict[country][coin_name][year]["uncropped"]:

                    if not coin_photo in catalog_dict[country][coin_name][year]["cropped"]:
                        continue

                    augmentation_path = os.path.join(catalog_path, "augmented", country, coin_name, year)
                    os.makedirs(augmentation_path, exist_ok=True)


                    cropped_coin_photo_path = os.path.join(catalog_path, country, coin_name, year, "cropped", coin_photo)
                    uncropped_coin_photo_path = os.path.join(catalog_path, country, coin_name, year, "uncropped", coin_photo)

                    # augment(augmentation_path, cropped_coin_photo_path, uncropped_coin_photo_path)
                    out.append((augmentation_path, uncropped_coin_photo_path, cropped_coin_photo_path))
    return out



class Worker:
    def __init__(self, name, augmentation_path, cropped_coin_photo_path, uncropped_coin_photo_path):
        self.name = name
        self.augmentation_path = augmentation_path
        self.cropped_coin_photo_path = cropped_coin_photo_path
        self.uncropped_coin_photo_path = uncropped_coin_photo_path
        _, self.country, self.coin, self.year, _, _ = split_path(uncropped_coin_photo_path)

    def run(self):
        worker_name = f"{COLOR_BLUE}Worker [{self.name}] sec"
        logging.info(f"{worker_name}: {COLOR_BLUE}started.{COLOR_RESET}")
        augment(self.augmentation_path, self.cropped_coin_photo_path, self.uncropped_coin_photo_path)
        logging.info(f"{worker_name}: {COLOR_BLUE}finished.{COLOR_RESET}")


class WorkerManager(QObject):
    def __init__(self, process_count):
        super().__init__()
        # Colored name for MainProcess (WorkerManager)
        self.name = f"{COLOR_BLUE}WorkerManager"
        self.max_processes = process_count
        self.running_processes = []  # Store currently running worker processes
        self.pending_tasks = []  # Store pending tasks as a queue

        # Timer to periodically check for completed processes
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_running_processes)
        self.timer.start(10)  # Check every 100 ms

    def run_workers(self, aug_tasks):
        # Queue up all tasks initially
        self.pending_tasks.extend(aug_tasks)
        self._assign_tasks()

    def _assign_tasks(self):
        # Assign tasks if there are available slots
        while len(self.running_processes) < self.max_processes and self.pending_tasks:
            augmentation_path, uncropped_coin_photo_path, cropped_coin_photo_path = self.pending_tasks.pop(0)
            _, country, coin, year, _, pic = split_path(uncropped_coin_photo_path)
            name = f"{country}/{coin}/{year}/{pic}"

            worker = Worker(name, augmentation_path, cropped_coin_photo_path, uncropped_coin_photo_path)

            # Start Worker in a new multiprocessing Process
            worker_process = Process(target=worker.run, name=f"{COLOR_GREEN}Worker [{name}]{COLOR_RESET}")
            worker_process.start()

            # Track the worker process
            self.running_processes.append(worker_process)
            logging.info(f"{self.name}: {COLOR_BLUE}Started Worker process for [{name}].{COLOR_RESET}")

    def _check_running_processes(self):
        # Check for completed processes
        for process in self.running_processes[:]:  # Copy list to allow modification
            if not process.is_alive():  # Process has finished
                process.join()  # Clean up the process
                self.running_processes.remove(process)
                logging.info(f"{self.name}: {COLOR_BLUE}Worker process completed and cleaned up.{COLOR_RESET}")

        # Assign more tasks if there are available slots
        self._assign_tasks()

        # Exit application if all tasks and processes are complete
        if not self.pending_tasks and not self.running_processes:
            logging.info(f"{self.name}: {COLOR_BLUE}All tasks completed. Exiting application.{COLOR_RESET}")
            self.timer.stop()
            QCoreApplication.quit()


if __name__ == "__main__":
    app = QCoreApplication(sys.argv)

    manager = WorkerManager(process_count=100)
    aug_tasks = get_augmentation_tasks()

    manager.run_workers(aug_tasks)

    sys.exit(app.exec())
