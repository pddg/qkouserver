from multiprocessing import Queue
from queue import Empty
from multiprocessing import Process
from logging import getLogger

import tweepy

from static import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET


class GetAuth(object):
    """
    Get authentication from twitter.com
    """

    def __init__(self):
        self.CK = CONSUMER_KEY
        self.CS = CONSUMER_SECRET
        self.AT = ACCESS_TOKEN
        self.AS = ACCESS_SECRET
        self.my_info = self.api.me()

    @property
    def api(self) -> tweepy.API:
        """
        Returns:
             tweepy.API object
        """
        return tweepy.API(auth_handler=self.auth, wait_on_rate_limit=True)

    @property
    def auth(self) -> tweepy.OAuthHandler:
        """
        Set AccessToken and AccessSecret to OAuthHandler.
        Returns:
             tweepy.OAuthHandler object
        """
        auth = tweepy.OAuthHandler(self.CK, self.CS)
        auth.set_access_token(self.AT, self.AS)
        return auth


class TweetProcess(Process):
    """
    This class' instance has Queue when created. Queue has tweet information. So tweet it until Queue become empty.
    """

    def __init__(self, que: Queue):
        """
        Args:
            que: queue.Queue object
        """
        super(TweetProcess, self).__init__()
        self.logger = getLogger(__name__)
        self.queue = que
        self.daemon = True
        self.get_auth = GetAuth()
        self.tweetable = False

    def run(self) -> None:
        """
        Get data from Queue, and tweet until Queue become empty
        """
        while True:
            try:
                data = self.queue.get()
                if data is None:
                    break
                self.logger.debug("[TWEET] " + data)
                if self.tweetable:
                    self.get_auth.api.update_status(status=data)
            except KeyboardInterrupt:
                pass
            # except Empty:
            #     break
            except Exception as e:
                self.logger.exception(e)
        self.logger.info("[Finish TweetThread]")
        exit()
