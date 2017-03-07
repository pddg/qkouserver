from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, WARNING
from logging.handlers import QueueHandler, RotatingFileHandler
from multiprocessing import Queue
import sys

from static import LOG_FORMAT


def configure_logger(log_level: int, echo: bool=True, file_log: bool=False, file_path: str="log") -> None:
    """
    Configure logging.Logger to log this app's behavior.

    Args:
        log_level: Set log level. 1 == DEBUG, 2 == INFO, 3 == WARNING
        echo: debug output into stdout
        file_log: ファイルへのロギングを有効化するフラグ
        file_path: ログファイルを格納するディレクトリへのパス
    """
    logger = getLogger()
    if echo:
        f_debug_handler = StreamHandler(sys.stdout)
        f_debug_handler.setFormatter(Formatter(LOG_FORMAT))
        if log_level == 1:
            f_debug_handler.setLevel(DEBUG)
        elif log_level == 2:
            f_debug_handler.setLevel(INFO)
        else:
            f_debug_handler.setLevel(WARNING)
        logger.addHandler(f_debug_handler)
    if file_log:
        if file_path[-1] == "/":
            raise IOError("Given parameter `{path}` is invalid. "
                          "Last character is must not be `/`.".format(path=file_path))
        rotate_debug_handler = RotatingFileHandler(file_path + "/debug.log", "a+", (2*1024*1024), 5)
        rotate_debug_handler.setFormatter(Formatter(LOG_FORMAT))
        rotate_debug_handler.setLevel(DEBUG)
        logger.addHandler(rotate_debug_handler)
        rotate_warn_handler = RotatingFileHandler(file_path + "/error.log", "a+", (2*1024*1024), 5)
        rotate_warn_handler.setFormatter(Formatter(LOG_FORMAT))
        rotate_warn_handler.setLevel(WARNING)
        logger.addHandler(rotate_warn_handler)
    f_error_handler = StreamHandler(sys.stderr)
    f_error_handler.setFormatter(Formatter(LOG_FORMAT))
    f_error_handler.setLevel(WARNING)
    logger.addHandler(f_error_handler)


def configure_queue_logger(queue: Queue):
    """
    Configure logger to use QueueHandler.

    Args:
        queue: multiprocessing.Queue object
    """
    handler = QueueHandler(queue)
    logger = getLogger()
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
