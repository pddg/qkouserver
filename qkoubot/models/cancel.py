from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean

from .utils import Base
from .abstract import QkouBase
from static import LEC_CANCEL_ID_TEMPLATE, LEC_CANCEL_TEMPLATE


class Cancel(Base, QkouBase):
    """
    Model for lecture cancellation. This model relate with subject model.
    """
    __tablename__ = 'lec_cancel'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=150))
    teacher = Column(String(length=150))
    day = Column(DateTime)
    abstract = Column(String(length=1000))
    first = Column(DateTime)
    week = Column(String(length=10))
    period = Column(String(length=10))
    unique_hash = Column(String(length=255), unique=True)
    created_at = Column(DateTime, default=datetime.now())
    is_deleted = Column(Boolean, unique=False, default=False)
    last_confirmed = Column(DateTime)

    def __init__(self, title: str, teacher: str, day: str, week: str, period: str,
                 abstract: str, first: str, created_at: datetime=datetime.now()):
        self.week = week
        self.period = period
        self.title = title
        self.teacher = teacher
        self.day = self.convert_datetime(day)
        self.abstract = abstract
        self.first = self.convert_datetime(first)
        self.unique_hash = self.make_unique_hash(title, teacher, week, period, first, day)
        self.created_at = created_at
        self.last_confirmed = created_at

    @property
    def table_name(self) -> str:
        return self.__tablename__

    @property
    def tweet_text(self) -> str:
        """
        create text to tweet
        the characters of tweet text should be under 140 characters
        """
        unformatted = self.__str__()
        num = LEC_CANCEL_ID_TEMPLATE.format(id=self.id)
        return unformatted[0:131] + num if len(unformatted) > 131 else unformatted + num

    def __str__(self) -> str:
        return LEC_CANCEL_TEMPLATE.format(subject=self.title, teacher=self.teacher,
                                          week=self.week, period=self.period,
                                          str_day=self.day.strftime("%Y/%m/%d"), abstract=self.abstract)

    def __repr__(self) -> str:
        return "<Cancel '{title}' '{week}' '{period}' '{date}'>".format(title=self.title,
                                                                        week=self.week,
                                                                        period=self.period,
                                                                        date=self.first.strftime("%Y/%m/%d"))
