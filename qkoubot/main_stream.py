from multiprocessing import Queue
from logging import getLogger

from .database import ReplyInfo, ReplyNews, ReplyCancel
from .network import GetAuth, tweet_assembler
from .validators import tweet_vars_validate


def stream_process(status_queue: Queue, auth: GetAuth):
    """
    ユーザーストリームを処理するプロセス．受信プロセスと処理プロセスを分離し，
    受信したStatusオブジェクトはQueueを介して渡される．
    """
    logger = getLogger("StreamProcess")
    logger.info('[Start Stream]')
    tweet_vars_validate()
    r_info = ReplyInfo()
    r_news = ReplyNews()
    r_cancel = ReplyCancel()
    while True:
        try:
            status = status_queue.get()
            judge, q_id = tweet_assembler(status, auth.api)
            if judge == 0:
                logger.debug('Send direct message about [Info] to {screen}'.format(screen=status.user.screen_name))
                text = r_info.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            elif judge == 1:
                logger.debug('Send direct message about [News] to {screen}'.format(screen=status.user.screen_name))
                text = r_news.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            elif judge == 2:
                logger.debug('Send direct message about [Cancel] to {screen}'.format(screen=status.user.screen_name))
                text = r_cancel.get_info_by_id(q_id)
                auth.api.send_direct_message(user_id=status.user.id, text=text)
            else:
                logger.debug('There are no information to search database.')
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.exception(e.args)
