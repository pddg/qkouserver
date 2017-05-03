from logging import getLogger
from multiprocessing import Queue

from .log_configures import configure_logger


def log_listener_process(queue: Queue, log_level: int, echo: bool, file_log: bool, file_path: str, prefix: str):
    """
    Configure logger at LogListenerProcess. Get log data from Queue, and handle it.

    Args:
        queue: multiprocessing.Queue object
        log_level: Set log level. 1 == DEBUG, 2 == INFO, 3 == WARNING
        echo: stdoutへログを出力するフラグ
        file_log: ログファイルへの記録を有効化
        file_path: ログファイルを格納するディレクトリのパス
        prefix: ログファイル名へのプレフィクス
    """
    path = file_path if file_path else "log"
    configure_logger(log_level, echo, file_log=file_log, file_path=path, prefix=prefix)
    while True:
        try:
            record = queue.get()
            if record is None:
                break
            logger = getLogger(record.name)
            logger.handle(record)
        except Exception as e:
            import sys
            import traceback
            print(e.args, file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
    print("[End ListenerProcess]")
