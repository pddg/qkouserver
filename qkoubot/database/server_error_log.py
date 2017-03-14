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
        self.newest_failure = self.get_newest_failure()  # type: Optional[ServerErrorLog]
        # 初期化時に古すぎるデータを無かったことにする
        if self.newest_failure is not None \
                and (self.last_confirmed - self.newest_failure.last_confirmed).total_seconds() > 3600:
            with Session() as session:
                session.add(self.newest_failure)
                self.newest_failure.is_fixed = True
                session.commit()
        self.current_status = self.newest_failure.is_fixed if self.newest_failure is not None else True

    @staticmethod
    def get_newest_failure() -> Optional[ServerErrorLog]:
        """
        最新のログイン失敗情報を取得．
        Returns:
            最新のログイン失敗情報．無ければNoneを返す．
        """
        with Session() as session:
            newest = session.query(ServerErrorLog)\
                .order_by(desc(ServerErrorLog.created_at))\
                .filter(ServerErrorLog.is_fixed is False)\
                .limit(1).first()  # type: Optional[ServerErrorLog]
        return newest

    def error_occurs(self, e: str):
        """
        エラー発生時に呼ばれる関数．
        current_statusに応じて新規作成または既存情報を更新．場合に応じてツイートするためにQueueに追加する．

        Args:
            e: Exceptionの中身
        """
        self.last_confirmed = datetime.now()
        do_tweet = self.create_new_failure_log(e, created_at=self.last_confirmed) if self.current_status else self.update_failure_log()
        if do_tweet and self.tweetable:
            self.queue.put(str(self.newest_failure))
        self.current_status = False
        self.logger.warning(self.newest_failure.__repr__())

    def create_new_failure_log(self, e: str, created_at: datetime) -> bool:
        """
        新規情報の作成．

        Args:
            e: Exceptionの中身
            created_at: 障害発生日時
        Returns:
            True
        """
        with Session() as session:
            latest = ServerErrorLog(e, created_at=created_at)
            session.add(latest)
            session.commit()
        self.newest_failure = latest
        return True

    def update_failure_log(self) -> bool:
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
        ログインに成功したときに呼ばれる．last_confirmedは必ず更新される．
        """
        now = datetime.now()
        self.last_confirmed = now
        if self.current_status is False:
            self.current_status = True
            with Session() as session:
                session.add(self.newest_failure)
                self.newest_failure.is_fixed = True
                self.newest_failure.fixed_at = now
                self.newest_failure.last_confirmed = now
                self.newest_failure.tweeted_at = now
                session.commit()
            if self.tweetable:
                self.queue.put(str(self.newest_failure))
            self.logger.info(self.newest_failure.__repr__())
