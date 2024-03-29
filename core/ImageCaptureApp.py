from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication

from core.CatalogHandler import CoinCatalogHandler
from core.catalog.Coin import Coin
from core.catalog.ImageCollector import ImageCollector
from core.cv2.CV2Module import CV2Module
from core.threading.signals import ThreadingSignals
from core.ui.DraggableCrossesOverlay import DraggableCrossesOverlay
from core.video.video import VideoStream

# from core.signals import CustomSignals
# from utils.CV2Module import CV2Module


signals = ThreadingSignals()


class ImageCaptureApp:
    def __init__(self) -> None:
        app = QApplication([])
        self.main_window = ImageCollector(signals=signals)

        self.video_stream = VideoStream(signals.frame_available, device=0)
        self.main_window.refresh_camera_combo_box(self.video_stream.available_camera_ids)
        self.video_stream.start()

        self.catalog_handler = CoinCatalogHandler(signals)
        self.catalog_handler.active_coin = self.catalog_handler.get_list_of_coins()[0]
        self.current_coin_photo_id: int = 0

        self.cv2_module = CV2Module()
        self.overlay = DraggableCrossesOverlay(signals, self.main_window.image_label)
        self.overlay.setGeometry(self.main_window.image_label.geometry())

        # signals.frame_available.connect(self.frame_update)
        signals.s_active_coin_changed.connect(self.change_active_coin)
        signals.s_save_picture_button_pressed.connect(self.save_coin_photo)
        signals.camera_reinit_signal.connect(self.video_stream_reinit)
        signals.s_active_tab_changed.connect(self.tab_change_routine)

        signals.s_coin_photo_id_changed.connect(self.show_catalog_coin_photo)

        signals.s_coin_vertices_update.connect(self.update_crossess_coordinates)
        signals.s_reset_vertices.connect(self.overlay.reset_vertices)

        self.main_window.show()
        self.refresh_coins_list()
        self.tab_change_routine()

        signals.s_catalog_changed.connect(self.refresh_coins_list)
        app.exec_()

    # def refresh_coins_combo_box(self):
    #     self.main_window.active_coin_combo_box.clear()
    #     coin_list: list[Coin] = self.catalog_handler.get_list_of_coins()
    #     self.main_window.refresh_coins_combo_box(coin_list)
    #
    #     try:
    #         current_idx: int = self.main_window.active_coin_combo_box.currentIndex()
    #         self.catalog_handler.set_active_coin(coin_list[current_idx])
    #         self.main_window.active_coin_combo_box.setCurrentIndex(current_idx)
    #         self.main_window.plainTextEdit.appendPlainText(f"Current coin: {self.catalog_handler.active_coin.name}")
    #     except Exception as ex:
    #         self.catalog_handler.active_coin_name = None

    def set_camera_combo_box(self, camera_list):
        self.main_window.camera_swich_combo_box.addItems(camera_list)

    def save_coin_photo(self):
        if self.catalog_handler.active_coin is not None:
            self.catalog_handler.add_coin_image(self.main_window.image_label.pixmap())

    def refresh_coins_list(self):
        coin_list: list[Coin] = self.catalog_handler.get_list_of_coins()

        # raising comboBox.currentIndexChanged isn't necessary while change is originating from main app not user
        self.main_window.active_coin_combo_box.blockSignals(True)
        self.main_window.refresh_coins_combo_box(coin_list=coin_list)
        self.main_window.set_active_coin(active_coin=self.catalog_handler.active_coin)
        self.main_window.active_coin_combo_box.blockSignals(False)

    def change_active_coin(self, new_active_coin: Coin):
        self.catalog_handler.set_active_coin(new_active_coin)
        self.refresh_coins_list()
        signals.s_append_info_text.emit(f"Active coin: {self.catalog_handler.active_coin.name}")
        if self.main_window.gallery_tab.isVisible():
            if len(self.catalog_handler.get_active_coin_dir_picture_files()) > 0:
                self.show_catalog_coin_photo(step=0)
        # self.tab_change_routine()

    def show_catalog_coin_photo(self, step: int = 0):
        self.current_coin_photo_id += step
        coin_image, vertices = self.catalog_handler.get_nth_coin_photo_from_catalog(self.current_coin_photo_id)
        width = self.main_window.image_label.width()
        height = self.main_window.image_label.height()
        crosses = [QPoint(x*width, y*height) for (x, y) in vertices]

        # self.overlay.init_image_with_vertices(self.catalog_handler.active_coin, self.current_coin_photo_id)
        self.overlay.crosses = crosses
        self.overlay.show()

        self.main_window.set_image(coin_image)

    def tab_change_routine(self):
        if self.main_window.camera_tab.isVisible():
            signals.s_append_info_text.emit(f"camera tab enabled")
            signals.frame_available.connect(self.frame_update)
            self.overlay.hide()
        elif self.main_window.gallery_tab.isVisible():
            self.current_coin_photo_id = 0
            signals.s_append_info_text.emit(f"gallery tab enabled")
            try:
                signals.frame_available.disconnect(self.frame_update)
            except:
                pass
            # taking coin photo from gallery
            if len(self.catalog_handler.get_active_coin_dir_picture_files()) > 0:
                self.show_catalog_coin_photo(step=0)

    def frame_update(self, frame):
        # if self.main_window.camera_tab.isVisible():
        (corners, _, _) = self.cv2_module.detect_markers_on_frame(frame)
        frame = self.cv2_module.colorize_markers_on_frame(frame=frame, corners=corners)
        self.main_window.set_image(frame)

    def video_stream_reinit(self, camera_id=0):
        self.video_stream.stop()
        self.video_stream = VideoStream(signals.frame_available, device=camera_id).start()

    def update_crossess_coordinates(self, points: list[QPoint]):
        # coin_image, vertices = self.catalog_handler.get_nth_coin_photo_from_catalog(self.current_coin_photo_id)
        # coin_image, vertices = self.catalog_handler.get_nth_coin_photo_from_catalog(self.current_coin_photo_id)
        width = self.main_window.image_label.width()
        height = self.main_window.image_label.height()
        crosses = [(point.x()/ width, point.y()/ height) for point in points]
        self.catalog_handler.set_coin_photo_vertices(self.current_coin_photo_id, crosses)
        self.catalog_handler.write_catalog()
        # crosses = [QPoint(x * width, y * height) for (x, y) in vertices]
