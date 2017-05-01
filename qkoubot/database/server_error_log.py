from datetime import datetime
from multiprocessing import Queue
from typing import Optional
from logging import getLogger
from sqlalchemy import desc

from qkoubot.models import ServerErrorLog, Session
from static import LOGIN_FAILURE_TWEET_INTERVAL


class LoginFailureLog(object):
    """
    ログイン試行に失敗したときに適切にロギングするためのクラス．
    self.newest_failureで常に最新の障害情報を保持する．
    """
    def __init__(self, queue: Queue):
        self.last_confirmed = datetime.now()
        self.tweetable = False
        self.logger = getLogger("LoginFailureLogger")
        self.queue = queue
        self.newest_failure = self.__get_newest_failure()  # type: ServerErrorLog

    def __get_newest_failure(self) -> ServerErrorLog:
        """
        最新のログイン失敗情報を取得．
        Returns:
            最新のログイン失敗情報．無ければNoneを返す．
        """
        def init() -> ServerErrorLog:
            """新しいサーバログオブジェクトを返す"""
            new = ServerErrorLog("init", created_at=self.last_confirmed)
            new.is_fixed = True
            session.add(new)
            session.commit()
            return new
        with Session() as session:
            newest = session.query(ServerErrorLog)\
                .order_by(desc(ServerErrorLog.created_at))\
                .limit(1).first()  # type: Optional[ServerErrorLog]
            if newest is None:
                self.logger.debug("Create new ServerErrorLog object.")
                return init()
            elif (self.last_confirmed - newest.last_confirmed).total_seconds() > 3600:
                # 古いデータは無かったことにする．
                self.logger.debug("Reset ServerErrorLog object. Last confirmation is 3600 seconds ago.")
                return init()
            else:
                return newest

    def __create_new_failure_log(self, e: str):
        """
        新規情報の作成．

        Args:
            e: Exceptionの中身
        """
        with Session() as session:
            latest = ServerErrorLog(e, created_at=self.last_confirmed)
            session.add(latest)
            session.commit()
        self.newest_failure = latest

    def __update_failure_log(self) -> bool:
        """
        ログイン失敗情報をアップデートする．

        Returns:
            最終ツイート時刻と現在時刻がLOGIN_FAILURE_TWEET_INTERVAL以上差があったときTrue．それ以外ではFalse．
        """
        with Session() as session:
            session.add(self.newest_failure)
            self.newest_failure.last_confirmed = self.last_confirmed
            if (self.last_confirmed - self.newest_failure.tweeted_at).total_seconds() > LOGIN_FAILURE_TWEET_INTERVAL:
                self.newest_failure.tweeted_at = self.last_confirmed
                session.commit()
                return True
            else:
                session.commit()
                return False

    def set_fixed(self):
        """
        ログインに成功したときに呼ばれる．
        """
        now = datetime.now()
        with Session() as session:
            session.add(self.newest_failure)
            if self.newest_failure.is_fixed:
                self.logger.debug("All login and scraping process are success.")
                self.newest_failure.last_confirmed = now
            else:
                self.logger.info("[RECOVERED] Error has been recovered at {t}"
                                 .format(t=now.strftime("%Y/%m/%d %H:%M:%S")))
                self.newest_failure.is_fixed = True
                self.newest_failure.fixed_at = now
                self.newest_failure.last_confirmed = now
                self.newest_failure.tweeted_at = now
                if self.tweetable:
                    self.queue.put(str(self.newest_failure))
            session.commit()

    def error_occurs(self, e: str):
        """
        エラー発生時に呼ばれる関数．
        最新のServerErrorLog.is_fixedに応じて新規作成または既存情報を更新．場合に応じてツイートするためにQueueに追加する．

        Args:
            e: Exceptionの中身
        """
        self.logger.warning("[ERROR] Login or scraping failure occurs.")
        self.last_confirmed = datetime.now()
        if self.newest_failure.is_fixed:
            self.__create_new_failure_log(e)
            update = True
        else:
            update = self.__update_failure_log()
        if self.tweetable and update:
            self.queue.put(str(self.newest_failure))
        self.logger.warning(self.newest_failure.__repr__())
