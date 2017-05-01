import asyncio
from logging import getLogger
from datetime import datetime
from multiprocessing import Queue

from .cron import TodayCancel
from .database import LoginFailureLog, add, update_info, delete_olds
from .network import login_and_get_html
from .scraper import scrape_process
from .models import Info, Cancel, News, Base, engine
from .validators import tweet_vars_validate, shibboleth_vars_validate, db_path_validate


def cron_process(failure_tweet: bool, tweet_queue: Queue):
    """
    通常の定期更新プロセス．SCRAPING_INTERVALごとにアクセスしてデータを更新する．
    """
    tweet_vars_validate()
    shibboleth_vars_validate()
    db_path_validate()
    Base.metadata.create_all(engine)
    logger = getLogger(__name__)
    logger.info('[Start CronProcess]')
    failure_logger = LoginFailureLog(tweet_queue)
    # ツイート機能の有効化
    failure_logger.tweetable = failure_tweet
    try:
        try:
            # Login and get html
            htmls = asyncio.get_event_loop().run_until_complete(login_and_get_html(logger))
            data_list_list = [scrape_process(html) for html in htmls]
            failure_logger.set_fixed()
        except Exception as e:
            logger.exception(e.args)
            failure_logger.error_occurs(str(e.args))
            return
        # ログインに成功し，HTMLを取得し，パースできた場合のみ
        # リストの平滑化してからforループ
        for data in [data for d_list in data_list_list for data in d_list]:
            if add(data):
                logger.info("[NEW] " + data.__repr__())
                tweet_queue.put(data.tweet_text)
            else:
                if isinstance(data, Info):
                    updated_id = update_info(data)
                    if updated_id:
                        data.id = updated_id
                        logger.info("[UPDATE] " + data.__repr__())
                        tweet_queue.put(data.tweet_text)
                    else:
                        logger.debug("[EXISTS] " + data.__repr__())
                else:
                    logger.debug("[EXISTS] " + data.__repr__())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e.args)
    finally:
        logger.info("Finish cron process at {t}.".format(t=datetime.now().strftime("%Y/%m/%d %H:%M:%S")))


def today_cancel_tweet(tweet_queue: Queue):
    tweet_vars_validate()
    Base.metadata.create_all(engine)
    logger = getLogger(__name__)
    logger.debug("[Start daily job]")
    try:
        daily_job = TodayCancel(tweet_queue)
        daily_job.tweet_today_cancel()
        for model in [Info, Cancel, News]:
            delete_olds(model)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info("[END Daily Job]")
