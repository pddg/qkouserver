import re
import time
from logging import getLogger
from multiprocessing import Queue, Process
from typing import Tuple

import tweepy

from .tweeter import GetAuth


class Listner(tweepy.streaming.StreamListener):
    """
    This class listen from userstream.
    """
    def __init__(self, queue: Queue, get_auth: GetAuth):
        super(Listner, self).__init__()
        self.queue = queue
        self.get_auth = get_auth
        self.my_info = self.get_auth.my_info
        self.logger = getLogger(__name__)

    def on_status(self, status):
        """
        Get status object from stream, put it to Queue.
        Args:
            status: tweepy.Status object.
        """
        if status.in_reply_to_user_id == self.my_info.id:
            self.logger.debug("Get reply on stream: " + status.text + "from: " + status.user.screen_name)
            self.queue.put(status)

    def on_error(self, status):
        """
        Get error status from stream. Logged it as exception.
        Args:
            status: status object?
        """
        self.logger.exception(status)


class StreamReceiverProcess(Process):
    """
    This class is StreamReceiver using Listener. If stream broken, retry to start stream infinitely.
    """
    def __init__(self, queue: Queue, get_auth: GetAuth):
        super(StreamReceiverProcess, self).__init__()
        self.daemon = True
        self.queue = queue
        self.logger = getLogger(__name__)
        self.auth_data = get_auth

    def run(self):
        l = Listner(self.queue, self.auth_data)
        stream = tweepy.Stream(self.auth_data.auth, l)
        while True:
            try:
                self.logger.info('Try to start receiving stream...')
                stream.userstream()
            except Exception as e:
                self.logger.exception(e.args)
                time.sleep(30)
                stream = tweepy.Stream(self.auth_data.auth, l)


def tweet_assembler(status, api) -> Tuple[int, int]:
    """
    statusオブジェクトを受け取ったとき，その内容にREPLY_ACTION_REGEXと合致する物があれば，そのリプライ元を辿ってツイートを取得．
    リプライ元に含まれるハッシュタグを抽出しidを取得する関数に渡す．
    Args:
        status: tweepy.Status object. get from userstream
        api: tweepy.API object. it use in order to get Bot's tweet relate to this conversation.
    Returns:
        Tuple of 'mode' and 'id' (both of it is int object).
        mode: 0 is Info. 1 is News. 2 is Cancel. 3 is None
        id: Scrape it from text. if there is no match, return 0.
    """
    logger = getLogger("TweetAssembler")
    from static import REPLY_ACTION_REGEX
    regex = REPLY_ACTION_REGEX
    if re.match(regex, status.text, re.U):
        logger.debug("in_reply_to_status is matched with REPLY_ACTION_REGEX")
        from_id = status.in_reply_to_status_id
        if from_id is None:
            return 3, 0
        from_status = api.get_status(from_id)
        logger.debug("Get tweet whose id is {from_id}".format(from_id=from_id))
        entities = from_status.entities['hashtags']
        if len(entities) > 0:
            tag = entities[0]['text']
            return judge(tag)
        else:
            return 3, 0


def judge(hashtag: str) -> Tuple[int, int]:
    """
    Classify tweet.
    Args:
         hashtag: Twitter hashtag
    Returns:
        Tuple of 'mode' and 'id' (both of it is int object).
        mode: 0 is Info. 1 is News. 2 is None
        id: Scrape it from text. if there is no match, return 0.
    """
    from static import LEC_INFO_ACTION_REGEX, NEWS_ACTION_REGEX, LEC_CANCEL_ACTION_REGEX
    info_num = re.search(LEC_INFO_ACTION_REGEX, hashtag)
    news_num = re.search(NEWS_ACTION_REGEX, hashtag)
    cancel_num = re.search(LEC_CANCEL_ACTION_REGEX, hashtag)
    if info_num:
        return 0, int(info_num.group())
    elif news_num:
        return 1, int(news_num.group())
    elif cancel_num:
        return 2, int(cancel_num.group())
    else:
        return 3, 0
