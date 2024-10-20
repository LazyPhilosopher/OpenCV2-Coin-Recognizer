from typing import Type

from PySide6.QtCore import QObject, Signal, QEventLoop, QTimer

from core.qt_threading.messages.MessageBase import MessageBase


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class CommonSignals(QObject):

    # Catalog handler
    catalog_handler_request = Signal(object)
    catalog_handler_response = Signal(object)

    # Processing Module
    processing_module_request = Signal(object)

    # Video thread
    video_thread_request = Signal(object)
    # video_thread_response = Signal(object)
    frame_available = Signal(object)

    def __init__(self):
        super().__init__()


def blocking_response_message_await(request_signal: Signal,
                                    request_message: MessageBase,
                                    response_signal: Signal,
                                    response_message_type: Type[MessageBase],
                                    timeout_ms: int = 1000):
    ret_val: MessageBase | None = None
    loop: QEventLoop = QEventLoop()

    def _message_type_check(message: MessageBase):
        nonlocal ret_val
        if isinstance(message, response_message_type):
            ret_val = message
            loop.quit()

    # Set up the timeout mechanism using QTimer
    timer = QTimer()
    timer.setSingleShot(True)
    timer.timeout.connect(loop.quit)

    response_signal.connect(_message_type_check)
    request_signal.emit(request_message)

    # Start the timer and the event loop
    timer.start(timeout_ms)
    loop.exec_()

    # Clean up
    response_signal.disconnect(_message_type_check)
    if timer.isActive():
        timer.stop()  # Stop the timer if the response was received before timeout

    return ret_val
