from PySide6.QtCore import Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QMainWindow, QLabel

from core.catalog.Coin import Coin
from core.qt_threading.common_signals import CommonSignals
from core.qt_threading.headers import RequestBase
from core.qt_threading.headers.RequestBase import Modules
from core.qt_threading.headers.catalog_handler.CatalogDictRequest import CatalogDictRequest
from core.qt_threading.headers.catalog_handler.CatalogDictResponse import CatalogDictResponse
from core.qt_threading.headers.catalog_handler.PictureRequest import PictureRequest
from core.qt_threading.headers.catalog_handler.PictureResponse import PictureResponse
from core.ui.pyqt6_designer.d_gallery_window import Ui_GalleryWindow


class ImageGalleryWindow(QMainWindow, Ui_GalleryWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # self._window: QMainWindow | None = None

        self.image_label = QLabel(self.image_frame)
        self.image_label.setGeometry(0, 0, self.image_frame.width(), self.image_frame.height())
        self.image_label.setScaledContents(True)  # Ensure image scales with QLabel
        # self.image_label.setPixmap(QPixmap("data\\debug_img.png"))
        self.new_coin_window = None

        self.qt_signals = CommonSignals()

        self.qt_signals.catalog_handler_request.emit(CatalogDictRequest(source=Modules.GALLERY_WINDOW))

        self.qt_signals.catalog_handler_response.connect(self.receive_request)

        self.catalog: dict | None = None

        self.coin_catalog_year_dropbox.currentIndexChanged.connect(self.year_dropbox_update_callback)
        self.coin_catalog_country_dropbox.currentIndexChanged.connect(self.country_dropbox_update_callback)
        self.coin_catalog_name_dropbox.currentIndexChanged.connect(self.coin_name_update_callback)
        self.next_button.clicked.connect(self.next_picture_button_callback)
        self.previous_button.clicked.connect(self.previous_picture_button_callback)

        self.image_idx = 0

    @Slot()
    def request_catalog_dict(self):
        # self.signals.request_cameras_ids.emit()
        self.qt_signals.catalog_handler_request.emit(CatalogDictRequest())
        # self.signals.catalog_handler_request.emit("camera request")

    @Slot()
    def receive_request(self, request: RequestBase):
        print("receive_request")
        if isinstance(request, CatalogDictResponse):
            print(f"[ImageGalleryWindow]: {request.catalog}")

            self.catalog = request.catalog
            self.set_year_dropbox_items()

            year = self.coin_catalog_year_dropbox.currentText()
            self.set_country_dropbox_items(year=year)

            country = self.coin_catalog_country_dropbox.currentText()
            self.coin_catalog_name_dropbox.addItems(self.catalog[year][country].keys())
        if isinstance(request, PictureResponse):
            picture = request.picture
            self.image_label.setPixmap(picture)
            # print(picture)

    def set_year_dropbox_items(self):
        self.coin_catalog_year_dropbox.blockSignals(True)
        self.coin_catalog_year_dropbox.clear()
        self.coin_catalog_year_dropbox.addItems(list(self.catalog.keys()))
        self.coin_catalog_year_dropbox.blockSignals(False)

    def set_country_dropbox_items(self, year: str):
        self.coin_catalog_country_dropbox.blockSignals(True)
        self.coin_catalog_country_dropbox.clear()
        self.coin_catalog_country_dropbox.addItems(list(self.catalog[year].keys()))
        self.coin_catalog_country_dropbox.blockSignals(False)

    def set_coin_name_dropbox_items(self, year: str, country: str):
        self.coin_catalog_name_dropbox.blockSignals(True)
        self.coin_catalog_name_dropbox.clear()
        self.coin_catalog_name_dropbox.addItems(self.catalog[year][country].keys())
        self.coin_catalog_name_dropbox.blockSignals(False)

    def year_dropbox_update_callback(self):
        self.set_country_dropbox_items(year=self.coin_catalog_year_dropbox.currentText())
        self.set_coin_name_dropbox_items(year=self.coin_catalog_year_dropbox.currentText(),
                                         country=self.coin_catalog_country_dropbox.currentText())
        self.request_picture()

    def country_dropbox_update_callback(self):
        self.set_coin_name_dropbox_items(year=self.coin_catalog_year_dropbox.currentText(),
                                         country=self.coin_catalog_country_dropbox.currentText())
        self.request_picture()

    def coin_name_update_callback(self):
        self.request_picture()

    def next_picture_button_callback(self):
        print(f"Next button")
        self.image_idx += 1
        self.request_picture()

    def previous_picture_button_callback(self):
        print(f"Previous button")
        self.image_idx -= 1
        self.request_picture()

    def request_picture(self):
        year = self.coin_catalog_year_dropbox.currentText()
        country = self.coin_catalog_country_dropbox.currentText()
        name = self.coin_catalog_name_dropbox.currentText()

        coin: Coin = self.catalog[year][country][name]
        self.image_idx %= len(coin.pictures.keys())
        picture: str = list(coin.pictures.keys())[self.image_idx]
        self.qt_signals.catalog_handler_request.emit(PictureRequest(coin=coin,
                                                                    picture=picture,
                                                                    source=Modules.GALLERY_WINDOW,
                                                                    destination=Modules.CATALOG_HANDLER))

    def receive_picture(self, picture: QPixmap):
        pass

