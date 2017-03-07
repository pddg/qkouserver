from multiprocessing import Queue
from logging import getLogger

from .database import ReplyInfo, ReplyNews, ReplyCancel
from .network import GetAuth, StreamReceiverProcess, tweet_assembler
from .validators import tweet_vars_validate


def stream_process():
    """
    ユーザーストリームを処理するプロセス．受信プロセスと処理プロセスを分離し，
    受信したStatusオブジェクトはQueueを介して渡される．
    """
    logger = getLogger("StreamProcess")
    logger.info('[Start Stream]')
    tweet_vars_validate()
    status_queue = Queue()
    auth = GetAuth()
    stream = StreamReceiverProcess(status_queue, auth)
    stream.start()
    r_info = ReplyInfo()
    r_news = ReplyNews()
    r_cancel = ReplyCancel()
    while True:
        try:
            status = status_queue.get()
            judge, q_id = tweet_assembler(status, auth.api)
            if judge == 0:
                logger.debug('send direct message [Info] to {screen}'.format(screen=status.user.screen_name))
                text = r_info.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            elif judge == 1:
                logger.debug('send direct message [News] to {screen}'.format(screen=status.user.screen_name))
                text = r_news.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            elif judge == 2:
                logger.debug('send direct message [Cancel] to {screen}'.format(screen=status.user.screen_name))
                text = r_cancel.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            else:
                logger.debug('there are no information to search database.')
        except Exception as e:
            logger.exception(e.args)
