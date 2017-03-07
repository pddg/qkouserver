from sqlalchemy import Column, String, Integer, DateTime, Boolean
from datetime import datetime

from .utils import Base
from .abstract import QkouBase
from static import NEWS_ID_TEMPLATE, NEWS_TEMPLATE_WITH_LINK, NEWS_TEMPLATE_WITHOUT_LINK


class News(Base, QkouBase):
    """
    Model for News.
    """
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first = Column(DateTime)
    detail = Column(String(length=2000))
    link = Column(String(length=500))
    unique_hash = Column(String(length=255), unique=True)
    created_at = Column(DateTime, default=datetime.now())
    is_deleted = Column(Boolean, unique=False, default=False)
    last_confirmed = Column(DateTime)

    def __init__(self, first: str, detail: str, link: str, created_at: datetime=datetime.now()):
        self.first = self.convert_datetime(first)
        self.detail = detail.replace("\t", "")
        self.link = link
        self.unique_hash = self.make_unique_hash(first, detail)
        self.created_at = created_at
        self.last_confirmed = created_at

    @staticmethod
    def convert_datetime(time: str) -> datetime:
        return datetime.strptime(time, "%Y.%m.%d")

    @property
    def table_name(self) -> str:
        return self.__tablename__

    @property
    def tweet_text(self) -> str:
        """
        Return:
            tweet text under 140 characters.
        """
        unformatted = self.__str__()
        num = NEWS_ID_TEMPLATE.format(id=self.id)
        return unformatted[0:131] + num if len(unformatted) > 131 else unformatted + num

    def __str__(self) -> str:
        str_first = self.first.strftime("%Y/%m/%d")
        if len(self.link) > 0:
            return NEWS_TEMPLATE_WITH_LINK.format(str_first=str_first, **self.__dict__)
        else:
            return NEWS_TEMPLATE_WITHOUT_LINK.format(str_first=str_first, **self.__dict__)

    def __repr__(self) -> str:
        return "<News '{first}' '{detail}'>".format(first=self.first.strftime("%Y/%m/%d"),
                                                    detail=self.detail[0:15])
