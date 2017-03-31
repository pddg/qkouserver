import os
from typing import List, Union
from ast import literal_eval

# dir name or file path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PRJ_DIR = os.path.dirname(BASE_DIR)
SQLITE_DIR_PATH = os.getenv("SQLITE_PATH", BASE_DIR)
SQLITE_PATH = "sqlite:///{path}".format(path=os.path.join(SQLITE_DIR_PATH, "sqlite.db"))

# MySQL
USE_MYSQL = literal_eval(os.getenv("USE_MYSQL", "False").capitalize())
MYSQL_USERNAME = os.getenv("MYSQL_USERNAME", None)
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", None)
MYSQL_HOST = os.getenv("MYSQL_HOST", None)
MYSQL_DATABASE_NAME = os.getenv("MYSQL_DATABASE_NAME", None)

if MYSQL_USERNAME and MYSQL_PASSWORD and MYSQL_HOST and MYSQL_DATABASE_NAME:
    MYSQL_PATH = 'mysql+pymysql://' + MYSQL_USERNAME + ":" + MYSQL_PASSWORD \
                 + "@" + MYSQL_HOST + "/" + MYSQL_DATABASE_NAME + "?charset=utf8"
else:
    MYSQL_PATH = None

# Twitter authentication
CONSUMER_KEY = os.getenv("CONSUMER_KEY", None)
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET", None)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", None)
ACCESS_SECRET = os.getenv("ACCESS_SECRET", None)

# Shibboleth authentication
SHIBBOLETH_USERNAME = os.getenv("SHIBBOLETH_USERNAME", None)
SHIBBOLETH_PASSWORD = os.getenv("SHIBBOLETH_PASSWORD", None)

# URLs
# SYLLABUS_URL = "http://www.syllabus.kit.ac.jp/"
LEC_INFO_URL = "https://portal.student.kit.ac.jp/ead/?c=lecture_information"
LEC_CANCEL_URL = "https://portal.student.kit.ac.jp/ead/?c=lecture_cancellation"
NEWS_URL = "https://portal.student.kit.ac.jp/"

# Other settings
# EXCEPTION_TITLES = ["English", "Reading", "Writing", "Basic", "Speaking", "Learning",
#                     "Advanced", "Intermediate", "Acquisition", "Communication"]

TESTING = literal_eval(os.getenv("TESTING", "False").capitalize())
INITIALIZE = literal_eval(os.getenv("INITIALIZE", "True").capitalize())

# EXPIRE_ON = int(os.getenv("EXPIRE_ON", "60"))
SCRAPING_INTERVAL = int(os.getenv("SCRAPING_INTERVAL", "300"))
LOGIN_FAILURE_TWEET_INTERVAL = int(os.getenv("LOGIN_FAILURE_TWEET_INTERVAL", "1800"))
DAILY_TWEET_HOUR = int(os.getenv("DAILY_TWEET_HOUR", "7"))
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(processName)s - %(levelname)s - %(message)s")
DEFAULT_LOG_LOCATION = os.getenv("LOG_LOCATION", "log")
REPLY_ACTION_REGEX = ".*(詳し|くわし).*"
# UNDEFINED = "-"
# UNKNOWN = "不明"
# INTENSIVE = "集中"

LEC_INFO_ID_TEMPLATE = " #lec{id}"
LEC_INFO_ACTION_REGEX = "(?<=lec)[0-9]+"
LEC_INFO_TEMPLATE = "講義名：{subject}\n" \
                    "講師名：{teacher}\n" \
                    "時限：{week} {period}限\n" \
                    "概要：{abstract}\n" \
                    "詳細：{detail}"

LEC_CANCEL_ID_TEMPLATE = " #cancel{id}"
LEC_CANCEL_ACTION_REGEX = "(?<=cancel)[0-9]+"
LEC_CANCEL_TEMPLATE = "講義名：{subject}\n" \
                      "講師名：{teacher}\n" \
                      "休講日：{str_day}\n" \
                      "時限：{week} {period}限\n" \
                      "概要：{abstract}"

NEWS_ID_TEMPLATE = " #news{id}"
NEWS_ACTION_REGEX = "(?<=news)[0-9]+"
NEWS_TEMPLATE_WITH_LINK = "掲載日：{str_first}\n発信課: {division}\n概要: {category}\n詳細：{detail}\nリンク：{link}"
NEWS_TEMPLATE_WITHOUT_LINK = "掲載日：{str_first}\n詳細：{detail}"

THERE_IS_NO_INFORMATION_MSG = "お問い合わせされた情報は現在存在しません．"
DATABASE_ERROR_MSG = "DBエラーです．管理者までご連絡ください．"

LOGIN_FAILURE_START_MSG = "[障害検知]\n障害検知時刻：{created_at}\n現在，学務課ホームページへのログインができない，" \
                          "または情報が正常に取得できないエラーが発生しています．"
LOGIN_FAILURE_CONTINUE_MSG = "[障害継続中]\n障害検知時刻: {created_at}\n最終確認時刻: {last_confirmed}\n" \
                             "学務課ホームページへログインできない，または情報が正常に取得できないエラーが継続中です．"
LOGIN_FAILURE_END_MSG = "[障害復旧]\n障害検知時刻: {created_at}\n復旧確認時刻: {fixed_at}\n" \
                        "学務課ホームページへのログイン及び情報の取得に成功しました．"
TODAY_CANCEL_TEMPLATE = "{date} 本日の休講\n{titles}"
TODAY_CANCEL_NONE_TEMPLATE = "{date} 本日休講はありません．"
TODAY_CANCEL_TEMPLATE_CONTINUE = "{date} 本日の休講 続き\n{titles}"
TODAY_IS_HOLIDAY_TEMPLATE = "{date} 今日は{holiday_name}です．{msg}"
HOLIDAY_MSG_ARRAY = ["レポートや課題は終わりましたか？有意義な祝日をお過ごしください．",
                     "進捗どうですか？",
                     "今日くらいはこのbotもお休みをいただいても良いですか？まぁダメですよね．",
                     "ところでこのbotはPythonというプログラミング言語で書かれています．せっかくの休日ですし新しいことを始めてみては？"]


def create_dict(keys: List[str], value_list: List[List[Union[str, int]]]) -> List[dict]:
    """
    Create dict with given keys.
    Args:
        keys: list of dict key
        value_list: list of list of dict value
    Returns:
        List of dict
    """
    return [{k: v for k, v in zip(keys, values)} for values in value_list]


# Test data
INFO_MODEL_KEYS = ["title", "teacher", "week", "period", "abstract", "detail", "first", "updated_date"]
INFO_MODEL_DATAS = [["休講情報bot入門", "pudding", "月", "1", "授業連絡", "上条ちゃん補習でーす", "2017/2/21", "2017/2/21"],
                    ["休講情報bot実践", "pudding", "月", "1~3", "授業連絡",
                     "上条ちゃん補習でーす．そしてこれは文字数のテストなのでーす．めんどいでーす誰かかわってくださーい．"
                     "お願いしまーす眠いでーーす．ほんまめんどいんやが？？？？？？？え？？？？？？？？",
                     "2017/2/21", "2017/2/21"],
                    ["休講情報API入門", "pudding", "火", "2", "授業連絡", "上条ちゃん補習でーす", "2017/2/18", "2017/2/18"],
                    ["休講情報Client実践", "pudding", "集中", "-", "授業連絡", "上条ちゃん補習でーす", "2017/2/23", "2017/2/23"]]
INFO_MODEL_DATA_DICTS = create_dict(INFO_MODEL_KEYS, INFO_MODEL_DATAS)

CANCEL_MODEL_KEYS = ["title", "teacher", "week", "period", "abstract", "day", "first"]
CANCEL_MODEL_DATAS = [["休講情報bot入門", "pudding", "月", "1", "-", "2017/3/3", "2017/2/21"],
                      ["休講情報bot実践", "pudding", "月", "1~3", "-", "2017/2/25", "2017/2/21"],
                      ["休講情報API入門", "pudding", "火", "2", "サボりたくなった", "2017/3/1", "2017/2/18"],
                      ["休講情報Client実践", "pudding", "集中", "-", "疲れた", "2017/4/1", "2017/2/23"]]
CANCEL_MODEL_DATA_DICTS = create_dict(CANCEL_MODEL_KEYS, CANCEL_MODEL_DATAS)

NEWS_MODEL_KEYS = ["first", "detail", "link", "division", "category"]
NEWS_MODEL_DATAS = [["2017.2.10", "2/21は情報工学課程の卒研発表の日です．", "http://hoge.hoge.com/fuga",
                     "〈学務課〉", "《-》"],
                    ["2017.2.12", "今日は文字数テストをしたいと思います．これは140文字を超えるように書いています．今はとても眠いです．"
                                  "テストを書く作業はとてもつらいので時給が欲しいという気持ちが高まっています．"
                                  "僕の脳内の仕様を読み取って良い感じにして欲しい…お願い…ソフトウェア工学の力で解決して欲しい…", "",
                     "〈学務課〉", "《-》"]]
NEWS_MODEL_DATA_DICTS = create_dict(NEWS_MODEL_KEYS, NEWS_MODEL_DATAS)
