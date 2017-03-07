from sqlalchemy import Column, String, Integer, DATETIME, Boolean
from datetime import datetime

from .utils import Base
from .abstract import QkouBase
from static import LEC_INFO_ID_TEMPLATE, LEC_INFO_TEMPLATE


class Info(Base, QkouBase):
    """
    Model for lecture information. This model relate with subject model.
    """
    __tablename__ = 'lec_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=150))
    teacher = Column(String(length=150))
    abstract = Column(String(length=40))
    detail = Column(String(length=2000))
    week = Column(String(length=10))
    period = Column(String(length=10))
    unique_hash = Column(String(length=255), unique=True)
    renew_hash = Column(String(length=255))
    first = Column(DATETIME)
    updated_date = Column(DATETIME)
    created_at = Column(DATETIME, default=datetime.now())
    last_confirmed = Column(DATETIME)
    is_deleted = Column(Boolean, unique=False, default=False)

    def __init__(self, title: str, teacher: str, week: str, period: str, abstract: str,
                 detail: str, first: str, updated_date: str, created_at: datetime=datetime.now()):
        self.week = week
        self.period = period
        self.title = title
        self.teacher = teacher
        self.abstract = abstract
        self.detail = detail
        self.first = self.convert_datetime(first)
        self.updated_date = self.convert_datetime(updated_date)
        self.unique_hash = self.make_unique_hash(title, teacher, week, period, abstract, first)
        self.renew_hash = self.make_unique_hash(detail, updated_date)
        self.created_at = created_at
        self.last_confirmed = created_at

    @property
    def table_name(self) -> str:
        """
        Return:
            table name
        """
        return self.__tablename__

    @property
    def tweet_text(self) -> str:
        """
        Return:
            tweet text under 140 characters.
        """
        unformatted = self.__str__()
        num = LEC_INFO_ID_TEMPLATE.format(id=self.id)
        return unformatted[0:131] + num if len(unformatted) > 131 else unformatted + num

    def __str__(self) -> str:
        return LEC_INFO_TEMPLATE.format(subject=self.title, teacher=self.teacher,
                                        week=self.week, period=self.period,
                                        abstract=self.abstract, detail=self.detail)

    def __repr__(self) -> str:
        return "<Info '{title}' '{week}' '{period}' '{date}'>".format(title=self.title,
                                                                      week=self.week,
                                                                      period=self.period,
                                                                      date=self.first.strftime("%Y/%m/%d"))
