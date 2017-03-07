from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from static import MYSQL_PATH, SQLITE_PATH, TESTING

Base = declarative_base()

DB_PATH = MYSQL_PATH if MYSQL_PATH else SQLITE_PATH
engine = create_engine(DB_PATH, echo=TESTING, pool_recycle=3600)
Sess = sessionmaker(bind=engine, expire_on_commit=False, autocommit=False)


class Session(object):

    def __init__(self):
        self.session = Sess()

    def __enter__(self):
        return self.session

    def __exit__(self, *exception):
        if exception[0] is not None:
            self.session.rollback()
        self.session.close()
