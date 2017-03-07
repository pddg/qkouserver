from sqlalchemy import Column, String, Integer, DATETIME, Boolean
from datetime import datetime

from .utils import Base
from static import LOGIN_FAILURE_START_MSG, LOGIN_FAILURE_CONTINUE_MSG, LOGIN_FAILURE_END_MSG


class ServerErrorLog(Base):
    """
    Logged time of fail down of KIT server.
    """
    __tablename__ = "server_error"

    id = Column(Integer, primary_key=True)
    message = Column(String(1000))
    is_fixed = Column(Boolean)
    fixed_at = Column(DATETIME, nullable=True)
    tweeted_at = Column(DATETIME)
    last_confirmed = Column(DATETIME)
    created_at = Column(DATETIME, default=datetime.now())

    def __init__(self, message: str, is_fixed: bool=False, created_at: datetime=datetime.now()):
        self.message = message
        self.is_fixed = is_fixed
        self.last_confirmed = created_at
        self.fixed_at = created_at
        self.tweeted_at = created_at
        self.created_at = created_at

    def __str__(self):
        time_format = "%Y/%m/%d %H:%M"
        created_at = self.created_at.strftime(time_format)
        if self.is_fixed is True:
            status = LOGIN_FAILURE_END_MSG.format(created_at=created_at, fixed_at=self.fixed_at.strftime(time_format))
        elif self.last_confirmed != self.fixed_at:
            status = LOGIN_FAILURE_CONTINUE_MSG.format(created_at=created_at,
                                                       last_confirmed=self.last_confirmed.strftime(time_format))
        else:
            status = LOGIN_FAILURE_START_MSG.format(created_at=created_at)
        return status
