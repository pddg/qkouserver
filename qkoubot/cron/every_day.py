import re
from datetime import datetime, timedelta
from logging import getLogger
from typing import List
from random import choice
from multiprocessing import Queue
from sqlalchemy import and_
import tweepy

from .jholiday import holiday_name
from qkoubot.models import Cancel, Session
from qkoubot.network import GetAuth
from static import DAILY_TWEET_HOUR, TODAY_CANCEL_TEMPLATE, TODAY_CANCEL_TEMPLATE_CONTINUE, \
    HOLIDAY_MSG_ARRAY, TODAY_IS_HOLIDAY_TEMPLATE, TODAY_CANCEL_NONE_TEMPLATE


class TodayCancel(object):

    def __init__(self, queue: Queue):
        self.last_tweet_date = datetime.now()
        self.today_job_is_done = False
        self.auth = GetAuth()
        self.api = self.auth.api
        self.queue = queue
        self.logger = getLogger(__name__)
        self.tweetable = False

    def __del_yday_tweet(self) -> bool:
        """
        前日にツイートした本日の休講ツイートを削除する関数．
        Returns:
            True: 削除に成功
        """
        # 昨日の日付を取得
        yesterday = (datetime.now() + timedelta(days=-1)).strftime("%Y/%m/%d")
        # TLの取得
        try:
            self.logger.debug("Try to get tweets...")
            tweets = tweepy.Cursor(self.api.user_timeline, id=self.auth.my_info.id).items(100)
        except Exception as e:
            self.logger.exception(e)
            return False
        results = [(tweet, re.match(yesterday, tweet.text)) for tweet in tweets]
        # 昨日の定期ツイートを削除
        for tweet, match in results:
            if match:
                try:
                    self.logger.debug("[DESTROY] tweet's id is {id}".format(id=tweet.id))
                    self.api.destroy_status(tweet.id)
                except Exception as e:
                    self.logger.exception(e)
                    return False
        # 一つでもマッチしていたらTrueを返す．
        for tweet, match in results:
            if match:
                return True
        return False

    def tweet_today_cancel(self) -> None:
        now = datetime.now()
        if self.tweetable and now.hour == DAILY_TWEET_HOUR and not self.today_job_is_done:
            if self.__del_yday_tweet():
                self.logger.debug("Deleted daily tweet of yesterday.")
            else:
                self.logger.warning("Could't find daily tweet of yesterday. Please confirm.")
            holiday = holiday_name(now.year, now.month, now.day)
            if holiday is None:
                contents = self.__get_sentence(now)
                for content in contents:
                    self.logger.debug("[TWEET] " + content)
                    self.queue.put(content)
            else:
                content = TODAY_IS_HOLIDAY_TEMPLATE.format(date=now.strftime("%Y/%m/%d"),
                                                           holiday_name=holiday, msg=choice(HOLIDAY_MSG_ARRAY))
                self.logger.debug("[TWEET] " + content)
                self.queue.put(content)
            self.today_job_is_done = True
            self.last_tweet_date = now
        passed_hour = (now - self.last_tweet_date).total_seconds() / 3600
        if passed_hour > 20:
            self.logger.debug("Make next day's cron job enable.")
            self.today_job_is_done = False

    @staticmethod
    def __convert_title_tweet(date: str, title_list: List[str]) -> List[str]:
        """
        休講の科目名一覧から今日の休講ツイートを作成する関数．最終的にツイートする内容をリストにして返す．
        Args:
            date: 今日の日付のstring
            title_list: 今日の休講科目の科目名リスト
        Return:
            ツイートする内容のリスト
        """
        if len(title_list) == 0:
            return [TODAY_CANCEL_NONE_TEMPLATE.format(date=date)]
        raw_sentence = TODAY_CANCEL_TEMPLATE.format(date=date, titles=", ".join(title_list))
        if len(raw_sentence) < 140:
            return [raw_sentence]
        remaining = 140 - len(TODAY_CANCEL_TEMPLATE_CONTINUE)
        result = []
        count = len(title_list)
        i = start = 0
        while count > 0:
            while True:
                if len(", ".join(title_list[start:i+1])) > remaining:
                    tmpl = TODAY_CANCEL_TEMPLATE if start == 0 else TODAY_CANCEL_TEMPLATE_CONTINUE
                    result.append(tmpl.format(date=date, titles=", ".join(title_list[start:i])))
                    start = i
                    break
                i += 1
            count -= start + 1
        return result

    def __get_sentence(self, now: datetime) -> List[str]:
        """
        日付を元に休講情報を取得．それをself.__convert_title_tweet()に渡してツイート内容を得る．
        Args:
            now: 今日の日付．datetime．
        Return:
            ツイートする内容のリスト
        """
        with Session() as session:
            today_cancels = session.query(Cancel).filter(and_(Cancel.day > (now + timedelta(days=-1)),
                                                              Cancel.day < (now + timedelta(days=1)))).all()
        return self.__convert_title_tweet(now.strftime("%Y/%m/%d"), [cancel.title for cancel in today_cancels])
