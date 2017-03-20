import time
import asyncio
from logging import getLogger
from multiprocessing import Queue

from .database import LoginFailureLog, add, update_info, delete_olds
from .network import login_and_get_html, TweetThread
from .scraper import scrape_process
from .cron import TodayCancel
from .models import Info, Cancel, News, Base, engine
from .validators import tweet_vars_validate, shibboleth_vars_validate, db_path_validate
from static import SCRAPING_INTERVAL


def cron_process(tweet: bool=False, failure_tweet: bool=True):
    """
    通常の定期更新プロセス．SCRAPING_INTERVALごとにアクセスしてデータを更新する．
    """
    tweet_vars_validate()
    shibboleth_vars_validate()
    db_path_validate()
    Base.metadata.create_all(engine)
    logger = getLogger(__name__)
    logger.info('[Start CronProcess]')
    tweet_queue = Queue()
    cron_job = TodayCancel(tweet_queue)
    tweet_thread = TweetThread(tweet_queue)
    tweet_thread.start()
    failure_logger = LoginFailureLog(tweet_queue)
    while True:
        try:
            loop = asyncio.get_event_loop()
            try:
                # Login and get html
                htmls = loop.run_until_complete(login_and_get_html(logger))
                failure_logger.set_fixed()
            except Exception as e:
                logger.exception(e.args)
                failure_logger.error_occurs(str(e.args))
            if failure_logger.current_status:
                # ログインに成功し，HTMLを取得できた場合のみ
                try:
                    data_list_list = [scrape_process(html) for html in htmls]
                except Exception as e:
                    logger.exception(e.args)
                    failure_logger.error_occurs(str(e.args))
                # リストの平滑化
                data_list = [data for d_list in data_list_list for data in d_list]
                for data in data_list:
                    try_to_add = add(data)
                    if try_to_add:
                        logger.info("[NEW] " + data.__repr__())
                        tweet_queue.put(data.tweet_text)
                    else:
                        if isinstance(data, Info):
                            try_to_update = update_info(data)
                            if try_to_update:
                                logger.info("[UPDATE] " + data.__repr__())
                                tweet_queue.put(data.tweet_text)
                            else:
                                logger.debug("[EXISTS] " + data.__repr__())
                        else:
                            logger.debug("[EXISTS] " + data.__repr__())
            for model in [Info, Cancel, News]:
                delete_olds(model)
            # 毎日の休講ツイートジョブ
            cron_job.tweet_today_cancel()
            if tweet:
                while not tweet_queue.empty():
                    # Queueの中身を消費しきるまで待機
                    time.sleep(1)
                # ツイート機能が有効（True）だった場合，各機能を有効化
                tweet_thread.tweetable = tweet
                cron_job.tweetable = tweet
                failure_logger.tweetable = failure_tweet
                tweet = False
                logger.info("Now completed preparing for tweet.")
        except Exception as e:
            logger.exception(e.args)
        finally:
            logger.debug("Sleep {min} minutes...".format(min=str(SCRAPING_INTERVAL / 60)))
            time.sleep(SCRAPING_INTERVAL)
