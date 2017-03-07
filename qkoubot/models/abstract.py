import hashlib
from datetime import datetime


class QkouBase(object):

    @staticmethod
    def convert_datetime(date: str) -> datetime:
        # convert from string to datetime
        return datetime.strptime(date, "%Y/%m/%d")

    @staticmethod
    def make_unique_hash(*args) -> str:
        # hash for identification
        return hashlib.sha256("".join(args).encode('utf-8')).hexdigest()

    @property
    def table_name(self):
        pass

    @property
    def tweet_text(self):
        pass
