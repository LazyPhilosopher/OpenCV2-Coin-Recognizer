# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'd_ImageCollector.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QLabel, QMainWindow, QPlainTextEdit, QPushButton,
    QSizePolicy, QSlider, QStatusBar, QTabWidget,
    QWidget)

class Ui_ImageCollector(object):
    def setupUi(self, ImageCollector):
        if not ImageCollector.objectName():
            ImageCollector.setObjectName(u"ImageCollector")
        ImageCollector.resize(870, 630)
        self.centralwidget = QWidget(ImageCollector)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(630, 445, 49, 16))
        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(610, 5, 16, 601))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(630, 5, 231, 401))
        self.camera_tab = QWidget()
        self.camera_tab.setObjectName(u"camera_tab")
        self.camera_swich_combo_box = QComboBox(self.camera_tab)
        self.camera_swich_combo_box.setObjectName(u"camera_swich_combo_box")
        self.camera_swich_combo_box.setGeometry(QRect(90, 10, 131, 21))
        self.label_2 = QLabel(self.camera_tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 61, 20))
        self.label_2.setAlignment(Qt.AlignCenter)
        self.save_photo_button = QPushButton(self.camera_tab)
        self.save_photo_button.setObjectName(u"save_photo_button")
        self.save_photo_button.setEnabled(True)
        self.save_photo_button.setGeometry(QRect(10, 50, 211, 31))
        self.save_photo_button.setCheckable(False)
        self.auto_mark_edges_checkbox = QCheckBox(self.camera_tab)
        self.auto_mark_edges_checkbox.setObjectName(u"auto_mark_edges_checkbox")
        self.auto_mark_edges_checkbox.setEnabled(False)
        self.auto_mark_edges_checkbox.setGeometry(QRect(10, 120, 201, 31))
        self.auto_mark_edges_checkbox.setCheckable(False)
        self.new_coin_button = QPushButton(self.camera_tab)
        self.new_coin_button.setObjectName(u"new_coin_button")
        self.new_coin_button.setEnabled(True)
        self.new_coin_button.setGeometry(QRect(10, 90, 211, 31))
        self.blur_kernel_slider = QSlider(self.camera_tab)
        self.blur_kernel_slider.setObjectName(u"blur_kernel_slider")
        self.blur_kernel_slider.setGeometry(QRect(89, 160, 131, 10))
        self.blur_kernel_slider.setOrientation(Qt.Horizontal)
        self.label_5 = QLabel(self.camera_tab)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(10, 160, 71, 10))
        self.blur_sigma_slider = QSlider(self.camera_tab)
        self.blur_sigma_slider.setObjectName(u"blur_sigma_slider")
        self.blur_sigma_slider.setGeometry(QRect(90, 180, 131, 10))
        self.blur_sigma_slider.setOrientation(Qt.Horizontal)
        self.canny_thr_1_slider = QSlider(self.camera_tab)
        self.canny_thr_1_slider.setObjectName(u"canny_thr_1_slider")
        self.canny_thr_1_slider.setGeometry(QRect(90, 200, 131, 10))
        self.canny_thr_1_slider.setOrientation(Qt.Horizontal)
        self.canny_thr_2_slider = QSlider(self.camera_tab)
        self.canny_thr_2_slider.setObjectName(u"canny_thr_2_slider")
        self.canny_thr_2_slider.setGeometry(QRect(90, 220, 131, 10))
        self.canny_thr_2_slider.setOrientation(Qt.Horizontal)
        self.dilate_1_slider = QSlider(self.camera_tab)
        self.dilate_1_slider.setObjectName(u"dilate_1_slider")
        self.dilate_1_slider.setGeometry(QRect(90, 240, 131, 10))
        self.dilate_1_slider.setOrientation(Qt.Horizontal)
        self.dilate_2_slider = QSlider(self.camera_tab)
        self.dilate_2_slider.setObjectName(u"dilate_2_slider")
        self.dilate_2_slider.setGeometry(QRect(90, 260, 131, 10))
        self.dilate_2_slider.setOrientation(Qt.Horizontal)
        self.erode_1_slider = QSlider(self.camera_tab)
        self.erode_1_slider.setObjectName(u"erode_1_slider")
        self.erode_1_slider.setGeometry(QRect(90, 280, 131, 10))
        self.erode_1_slider.setOrientation(Qt.Horizontal)
        self.label_6 = QLabel(self.camera_tab)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 180, 71, 10))
        self.label_7 = QLabel(self.camera_tab)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 200, 71, 10))
        self.label_8 = QLabel(self.camera_tab)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 220, 71, 10))
        self.label_9 = QLabel(self.camera_tab)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 240, 71, 10))
        self.label_10 = QLabel(self.camera_tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 260, 71, 10))
        self.label_11 = QLabel(self.camera_tab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(10, 280, 71, 10))
        self.erode_2_slider = QSlider(self.camera_tab)
        self.erode_2_slider.setObjectName(u"erode_2_slider")
        self.erode_2_slider.setGeometry(QRect(90, 300, 131, 10))
        self.erode_2_slider.setOrientation(Qt.Horizontal)
        self.label_12 = QLabel(self.camera_tab)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(10, 300, 71, 10))
        self.dilate_iter_slider = QSlider(self.camera_tab)
        self.dilate_iter_slider.setObjectName(u"dilate_iter_slider")
        self.dilate_iter_slider.setGeometry(QRect(90, 320, 131, 10))
        self.dilate_iter_slider.setOrientation(Qt.Horizontal)
        self.erode_iter_slider = QSlider(self.camera_tab)
        self.erode_iter_slider.setObjectName(u"erode_iter_slider")
        self.erode_iter_slider.setGeometry(QRect(90, 340, 131, 10))
        self.erode_iter_slider.setOrientation(Qt.Horizontal)
        self.label_13 = QLabel(self.camera_tab)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(10, 320, 71, 10))
        self.label_14 = QLabel(self.camera_tab)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(10, 340, 71, 10))
        self.tabWidget.addTab(self.camera_tab, "")
        self.gallery_tab = QWidget()
        self.gallery_tab.setObjectName(u"gallery_tab")
        self.vertices_reset_button = QPushButton(self.gallery_tab)
        self.vertices_reset_button.setObjectName(u"vertices_reset_button")
        self.vertices_reset_button.setGeometry(QRect(10, 50, 211, 31))
        self.next_gallery_photo_button = QPushButton(self.gallery_tab)
        self.next_gallery_photo_button.setObjectName(u"next_gallery_photo_button")
        self.next_gallery_photo_button.setGeometry(QRect(120, 10, 101, 31))
        self.previous_gallery_photo_button = QPushButton(self.gallery_tab)
        self.previous_gallery_photo_button.setObjectName(u"previous_gallery_photo_button")
        self.previous_gallery_photo_button.setGeometry(QRect(10, 10, 91, 31))
        self.tabWidget.addTab(self.gallery_tab, "")
        self.coin_tab = QWidget()
        self.coin_tab.setObjectName(u"coin_tab")
        self.tabWidget.addTab(self.coin_tab, "")
        self.coin_catalog_year_dropbox = QComboBox(self.centralwidget)
        self.coin_catalog_year_dropbox.setObjectName(u"coin_catalog_year_dropbox")
        self.coin_catalog_year_dropbox.setGeometry(QRect(700, 415, 161, 22))
        self.video_frame = QFrame(self.centralwidget)
        self.video_frame.setObjectName(u"video_frame")
        self.video_frame.setGeometry(QRect(10, 5, 600, 600))
        self.video_frame.setFrameShape(QFrame.Panel)
        self.video_frame.setFrameShadow(QFrame.Sunken)
        self.video_frame.setLineWidth(1)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(630, 475, 61, 16))
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(630, 500, 231, 101))
        self.plainTextEdit.setReadOnly(True)
        self.coin_catalog_country_dropbox = QComboBox(self.centralwidget)
        self.coin_catalog_country_dropbox.setObjectName(u"coin_catalog_country_dropbox")
        self.coin_catalog_country_dropbox.setGeometry(QRect(700, 445, 161, 22))
        self.coin_catalog_name_dropbox = QComboBox(self.centralwidget)
        self.coin_catalog_name_dropbox.setObjectName(u"coin_catalog_name_dropbox")
        self.coin_catalog_name_dropbox.setGeometry(QRect(700, 475, 161, 22))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(630, 420, 31, 16))
        ImageCollector.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ImageCollector)
        self.statusbar.setObjectName(u"statusbar")
        ImageCollector.setStatusBar(self.statusbar)

        self.retranslateUi(ImageCollector)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(ImageCollector)
    # setupUi

    def retranslateUi(self, ImageCollector):
        ImageCollector.setWindowTitle(QCoreApplication.translate("ImageCollector", u"Image Collector", None))
        self.label_3.setText(QCoreApplication.translate("ImageCollector", u"Country", None))
        self.label_2.setText(QCoreApplication.translate("ImageCollector", u"Camera", None))
        self.save_photo_button.setText(QCoreApplication.translate("ImageCollector", u"New Photo", None))
        self.auto_mark_edges_checkbox.setText(QCoreApplication.translate("ImageCollector", u"auto-mark coin edges", None))
        self.new_coin_button.setText(QCoreApplication.translate("ImageCollector", u"New Coin", None))
        self.label_5.setText(QCoreApplication.translate("ImageCollector", u"Blur Kernel", None))
        self.label_6.setText(QCoreApplication.translate("ImageCollector", u"Blur Sigma", None))
        self.label_7.setText(QCoreApplication.translate("ImageCollector", u"Canny Thr 2", None))
        self.label_8.setText(QCoreApplication.translate("ImageCollector", u"Canny Thr 2", None))
        self.label_9.setText(QCoreApplication.translate("ImageCollector", u"Dilate Kernel1", None))
        self.label_10.setText(QCoreApplication.translate("ImageCollector", u"Dilate Kernel2", None))
        self.label_11.setText(QCoreApplication.translate("ImageCollector", u"Erode Kernel1", None))
        self.label_12.setText(QCoreApplication.translate("ImageCollector", u"Erode Kernel2", None))
        self.label_13.setText(QCoreApplication.translate("ImageCollector", u"Dilate Iter", None))
        self.label_14.setText(QCoreApplication.translate("ImageCollector", u"Erode Iter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.camera_tab), QCoreApplication.translate("ImageCollector", u"Camera", None))
        self.vertices_reset_button.setText(QCoreApplication.translate("ImageCollector", u"Reset Coin Vertices", None))
        self.next_gallery_photo_button.setText(QCoreApplication.translate("ImageCollector", u"Next Photo", None))
        self.previous_gallery_photo_button.setText(QCoreApplication.translate("ImageCollector", u"Previous Photo", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.gallery_tab), QCoreApplication.translate("ImageCollector", u"Gallery", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.coin_tab), QCoreApplication.translate("ImageCollector", u"Coin ", None))
        self.label_4.setText(QCoreApplication.translate("ImageCollector", u"Coin name", None))
        self.plainTextEdit.setPlainText("")
        self.label.setText(QCoreApplication.translate("ImageCollector", u"Year", None))
    # retranslateUi

