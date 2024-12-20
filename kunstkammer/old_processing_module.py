import os

import numpy as np
from PySide6.QtCore import QObject, QThread
from PySide6.QtWidgets import QApplication
from skimage import transform, filters, exposure, util

from core.qt_communication.base import *
from core.qt_communication.messages.processing_module.Requests import *
from core.qt_communication.messages.processing_module.Responses import *
from core.utilities.helper import qimage_to_cv2, remove_background_rembg, cv2_to_qimage, \
    parse_directory_into_dictionary


class ProcessingModule(QObject):

    def __init__(self):
        super().__init__()

        self.is_running = False
        self.is_processing = False
        self.main_thread = QThread()
        self.qt_signals = CommonSignals()
        self.qt_signals.processing_module_request.connect(self.handle_request)

    def start_process(self):
        self.moveToThread(self.main_thread)
        self.main_thread.started.connect(self.worker)
        self.main_thread.start()
        self.is_running = True

    def worker(self):
        while self.is_running:
            QApplication.processEvents()

    def handle_request(self, request: MessageBase):
        request_handlers = {
            RemoveBackgroundRequest: self._handle_remove_background,
            AugmentCoinCatalogRequest: self._handle_catalog_augmentation_request
        }

        handler = request_handlers.get(type(request), None)
        if handler:
            if self.is_processing:
                return

            self.is_processing = True
            handler(request)
            self.is_processing = False

    def _handle_remove_background(self, request: RemoveBackgroundRequest):
        image = qimage_to_cv2(request.picture)
        img_no_bg = remove_background_rembg(image)
        self.qt_signals.processing_module_request.emit(
            ProcessedImageResponse(image=cv2_to_qimage(img_no_bg),
                                   source=Modules.PROCESSING_MODULE,
                                   destination=request.source))

    def _handle_catalog_augmentation_request(self, request: AugmentCoinCatalogRequest):
        catalog_dict = parse_directory_into_dictionary(request.catalog_path)
        os.makedirs(os.path.join(request.catalog_path, "augmented"), exist_ok=True)

        for country in catalog_dict.keys():
            for coin_name in catalog_dict[country].keys():
                for year in catalog_dict[country][coin_name].keys():
                    os.makedirs(os.path.join(request.catalog_path, country, coin_name, year), exist_ok=True)

                    for coin_photo in catalog_dict[country][coin_name][year]["uncropped"]:

                        if not coin_photo in catalog_dict[country][coin_name][year]["cropped"]:
                            continue

                        cropped_coin_photo_path = os.path.join(request.catalog_path, country, coin_name, year,
                                                               "cropped", coin_photo)
                        uncropped_coin_photo_path = os.path.join(request.catalog_path, country, coin_name, year,
                                                                 "uncropped", coin_photo)

                        os.makedirs(os.path.join(request.catalog_path, "augmented", country, coin_name, year),
                                    exist_ok=True)

                        cv2_uncropped_image: np.ndarray = qimage_to_cv2(QImage(uncropped_coin_photo_path))
                        cv2_cropped_image: np.ndarray = qimage_to_cv2(QImage(cropped_coin_photo_path))

                        # Transformations
                        for i in range(10):
                            image = cv2_to_qimage(cv2_uncropped_image)
                            image.save(
                                os.path.join(request.catalog_path, "augmented", country, coin_name, year,
                                             f"{i}_full.png"))

                            image = cv2_to_qimage(cv2_cropped_image)
                            image.save(
                                os.path.join(request.catalog_path, "augmented", country, coin_name, year,
                                             f"{i}_hue.png"))

