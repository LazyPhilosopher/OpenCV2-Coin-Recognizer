from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QGraphicsOpacityEffect, QStackedLayout


class ImageFrame(QFrame):
    def __init__(self, video_frame: QFrame):
        super().__init__(video_frame.parent())

        self.cropped_image: QPixmap | None = None
        self.uncropped_image: QPixmap | None = None

        self.front_image_label = QLabel(self)
        self.front_image_label.setScaledContents(True)
        self.background_image_label = QLabel(self)
        self.background_image_label.setScaledContents(True)

        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0.5)  # 50% transparent
        self.background_image_label.setGraphicsEffect(opacity_effect)
        self.front_image_label.setGraphicsEffect(opacity_effect)

        layout = QStackedLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self.front_image_label)
        layout.addWidget(self.background_image_label)

        self.setLayout(layout)
        self.clone_properties_from(video_frame)
        video_frame.deleteLater()

    def clone_properties_from(self, other_frame):
        if isinstance(other_frame, QFrame):
            geometry = other_frame.geometry()
            frame_shape = other_frame.frameShape()
            frame_shadow = other_frame.frameShadow()
            self.setGeometry(geometry)
            self.setFrameShape(frame_shape)
            self.setFrameShadow(frame_shadow)

    def set_image(self, uncropped_image: QImage, cropped_image: QImage | None):
        self.cropped_image = cropped_image
        self.uncropped_image = uncropped_image

        if cropped_image is not None:
            self.front_image_label.setPixmap(QPixmap(cropped_image))
            self.background_image_label.setPixmap(QPixmap(uncropped_image))
        else:
            self.front_image_label.setPixmap(QPixmap(uncropped_image))

    # def QPixmapToArray(self, pixmap):
    #     ## Get the size of the current pixmap
    #     size = pixmap.size()
    #     h = size.width()
    #     w = size.height()
    #
    #     ## Get the QImage Item and convert it to a byte string
    #     qimg = pixmap.toImage()
    #     byte_str = qimg.bits().tobytes()
    #
    #     ## Using the np.frombuffer function to convert the byte string into an np array
    #     img = np.frombuffer(byte_str, dtype=np.uint8).reshape((w, h, 4))
    #
    #     return img
