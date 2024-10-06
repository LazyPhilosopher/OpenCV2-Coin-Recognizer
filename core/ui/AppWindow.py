from PySide6.QtWidgets import QMainWindow

from core.ui.pyqt6_designer.d_main_window import Ui_MainWindow

from core.ui.ImageGalleryWindow import ImageGalleryWindow
from core.ui.ImageCollector import ImageCollector


class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._window: QMainWindow | None = None

        self.AddImageButton.clicked.connect(self.add_image_button_routine)
        self.ImageGalleryButton.clicked.connect(self.image_gallery_button_routine)

    def add_image_button_routine(self):
        self._window = ImageCollector()
        self._window.show()
        self.centralwidget.setEnabled(False)
        self._window.closeEvent = self._enable_central_widget

    def image_gallery_button_routine(self):
        self._window = ImageGalleryWindow()
        self._window.show()
        self.centralwidget.setEnabled(False)
        self._window.closeEvent = self._enable_central_widget

    def _enable_central_widget(self, event):
        """Re-enable the central widget when AddNewImageWindow is closed."""
        self.centralwidget.setEnabled(True)
        event.accept()



