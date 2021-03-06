import argparse
from multiprocessing import Queue, Process
from logging import getLogger


def main():
    parser = argparse.ArgumentParser(
        description="QkouBot is an application for KIT students. This automatically collect and "
                    "redistribute information and cancellation of lectures. QkouBot detect update of information "
                    "and tweet it."
    )
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("-v",
                               "--verbose",
                               dest="verbose",
                               default=False,
                               help="Default logging output is above WARNING level to stderr. "
                                    "If this option enabled, logging output is above INFO level to stdout by default."
                                    "You can change its level using `-l` or `--log-level` option.",
                               action="store_true"
                               )
    common_parser.add_argument("-l",
                               "--log-level",
                               dest="log_level",
                               default=[2],
                               type=int,
                               nargs=1,
                               choices=[1, 2, 3],
                               help="Choose a log level. 1: debug, 2: info, 3: warning. Default value is 2"
                               )
    common_parser.add_argument("--ini",
                               dest="ini",
                               type=str,
                               help="Read `*.ini` file and overwrite environment variables."
                               )
    common_parser.add_argument("--file-log-enable",
                               dest="file_log",
                               default=False,
                               help="Enable logging to `*.log` file. "
                                    "These files are save into `log` directory by default.",
                               action="store_true"
                               )
    common_parser.add_argument("--log-path",
                               dest="log_path",
                               default="log",
                               type=str,
                               help="Specify location of `*.log` file."
                               )
    sub_parser = parser.add_subparsers(help="sub commands help")
    bot_parser = sub_parser.add_parser("qkoubot", help="Start QkouBot command", parents=[common_parser])
    bot_parser.add_argument("-t",
                            "--tweet",
                            dest="tweet",
                            default=False,
                            help="Enable tweet update of any information.",
                            action="store_true"
                            )
    bot_parser.add_argument("--without-failure",
                            dest="without_f",
                            default=True,
                            action="store_false",
                            help="Tweet update of information, but do not tweet login failure information."
                            )
    bot_parser.set_defaults(func=bot)

    stream_parser = sub_parser.add_parser("stream", help="Start stream processing", parents=[common_parser])
    stream_parser.set_defaults(func=stream)

    today_job_parser = sub_parser.add_parser("dailyjob", help="Run daily job", parents=[common_parser])
    today_job_parser.add_argument("-t",
                                  "--tweet",
                                  dest="tweet",
                                  default=False,
                                  help="Enable tweet update of any information.",
                                  action="store_true"
                                  )
    today_job_parser.set_defaults(func=daily_job)
    args = parser.parse_args()
    if args.ini is not None:
        config_parse(args.ini)
    args.func(args)


def bot(args):
    from log_modules import log_listener_process, configure_queue_logger
    from qkoubot import cron_process, TweetProcess
    log_queue = Queue()
    tweet_queue = Queue()
    log_listener = Process(target=log_listener_process,
                           args=(log_queue, args.log_level[0], args.verbose, args.file_log, args.log_path, "bot"),
                           name="LogListenerProcess")
    log_listener.start()
    configure_queue_logger(queue=log_queue)
    logger = getLogger("Manage")
    logger.info("launching on QkouBot")
    tweet_process = TweetProcess(tweet_queue)
    tweet_process.tweetable = args.tweet
    tweet_process.start()
    try:
        cron_process(args.without_f, tweet_queue)
    except KeyboardInterrupt:
        from static import TESTING
        if TESTING:
            from qkoubot.models import Base, engine
            logger.info("Dropping Database ...")
            Base.metadata.drop_all(engine)
            logger.info("Complete.")
    except (AssertionError, FileNotFoundError, KeyError) as e:
        logger.exception(e.args)
    except Exception as e:
        logger.exception(e.args)
    finally:
        tweet_queue.put(None)
        tweet_process.join()
        log_queue.put(None)
        log_listener.join()
        exit()


def stream(args):
    from log_modules import log_listener_process, configure_queue_logger
    from qkoubot import stream_process, GetAuth, StreamReceiverProcess
    log_queue = Queue(-1)
    log_listener = Process(target=log_listener_process,
                           args=(log_queue, args.log_level[0], args.verbose, args.file_log, args.log_path, "stream"),
                           name="LogListenerProcess")
    log_listener.start()
    configure_queue_logger(queue=log_queue)
    logger = getLogger("Manage")
    logger.info("launching on QkouBot Stream Process")
    status_queue = Queue()
    auth = GetAuth()
    stream_receive_process = StreamReceiverProcess(status_queue, auth)
    stream_receive_process.start()
    try:
        stream_process(status_queue=status_queue, auth=auth)
    except KeyboardInterrupt:
        from static import TESTING
        if TESTING:
            from qkoubot.models import Base, engine
            Base.metadata.drop_all(engine)
            logger.info("Database was dropped.")
    except (AssertionError, FileNotFoundError, KeyError) as e:
        logger.exception(e.args)
    except Exception as e:
        logger.exception(e.args)
    finally:
        log_queue.put(None)
        log_listener.join()
        exit()


def daily_job(args):
    import time
    time.sleep(30)
    from log_modules import log_listener_process, configure_queue_logger
    from qkoubot import today_cancel_tweet, TweetProcess
    log_queue = Queue()
    tweet_queue = Queue()
    log_listener = Process(target=log_listener_process,
                           args=(log_queue, args.log_level[0], args.verbose, args.file_log, args.log_path, "daily"),
                           name="LogListenerProcess")
    log_listener.start()
    configure_queue_logger(log_queue)
    logger = getLogger(__name__)
    tweet_process = TweetProcess(tweet_queue)
    tweet_process.tweetable = args.tweet
    tweet_process.start()
    try:
        today_cancel_tweet(tweet_queue)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.exception(e)
    finally:
        tweet_queue.put(None)
        tweet_process.join()
        log_queue.put(None)
        log_listener.join()
        exit()


def config_parse(path: str) -> None:
    import os
    from configparser import ConfigParser
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    sections = [
        {
            "section": "mysql",
            "keys": ["MYSQL_USERNAME", "MYSQL_PASSWORD", "MYSQL_HOST", "MYSQL_DATABASE_NAME"]
        },
        {
            "section": "shibboleth",
            "keys": ["SHIBBOLETH_USERNAME", "SHIBBOLETH_PASSWORD"]
        },
        {
            "section": "twitter",
            "keys": ["CONSUMER_KEY", "CONSUMER_SECRET", "ACCESS_TOKEN", "ACCESS_SECRET"]
        },
        {
            "section": "other",
            "keys": ["TESTING", "SCRAPING_INTERVAL", "LOGIN_FAILURE_TWEET_INTERVAL",
                     "DAILY_TWEET_HOUR", "SQLITE_PATH", "LOG_LOCATION"]
        }
    ]
    section_titles = [section["section"] for section in sections]
    parser = ConfigParser()
    parser.read(path)
    for section in parser.sections():
        if section not in section_titles:
            raise KeyError(section + " is invalid section.")
        this_section = [sec for sec in sections if sec["section"] == section][0]
        for key, value in dict(parser.items(section)).items():
            if key.upper() not in this_section["keys"]:
                raise KeyError(key + " is invalid key name.")
            os.environ[key.upper()] = value

if __name__ == '__main__':
    main()
