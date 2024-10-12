from PySide6.QtCore import QPoint
from PySide6.QtGui import QPixmap, QImage

from core.qt_threading.messages.MessageBase import MessageBase


class DoNothingRequest(MessageBase):
    def __init__(self,  image: QImage, source=None, destination=None):
        super().__init__()
        self.image = image
        self.source = source
        self.destination = destination


class GrayscalePictureRequest(MessageBase):
    def __init__(self,  image: QImage, source=None, destination=None):
        super().__init__()
        self.image = image
        self.source = source
        self.destination = destination


class BorderDetectionRequest(MessageBase):
    def __init__(self,  picture: QImage, param_dict: dict, source=None, destination=None):
        super().__init__()
        self.picture = picture
        self.param_dict = param_dict
        self.source = source
        self.destination = destination


class RemoveBackgroundRequest(MessageBase):
    def __init__(self,  picture: QImage, param_dict: dict, source=None, destination=None):
        super().__init__()
        self.picture = picture
        self.param_dict = param_dict
        self.source = source
        self.destination = destination


class RemoveBackgroundVerticesRequest(MessageBase):
    def __init__(self,  picture: QImage, qpoint_vertices: list[QPoint], source=None, destination=None):
        super().__init__()
        self.picture = picture
        self.qpoint_vertices = qpoint_vertices
        self.source = source
        self.destination = destination
