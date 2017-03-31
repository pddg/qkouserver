import unittest
from datetime import datetime, timedelta
from nose.tools import eq_, raises, ok_
from sqlalchemy.exc import IntegrityError

from qkoubot.models import News, Session, Base, engine
from .utils import insert_all, delete_all, query_to_dict
from static import NEWS_MODEL_DATA_DICTS


class TestInfoModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        ok_(insert_all(News, NEWS_MODEL_DATA_DICTS))

    def tearDown(self):
        ok_(delete_all(News))

    def doCleanups(self):
        delete_all(News)

    def test_inserted_data_is_correct(self):
        with Session() as session:
            for info in NEWS_MODEL_DATA_DICTS:
                inserted = session.query(News).filter_by(first=datetime.strptime(info["first"], "%Y.%m.%d")).first()
                inserted_dict = query_to_dict(inserted)
                eq_(info["link"], inserted_dict["link"])
                eq_(info["detail"], inserted_dict["detail"])
                eq_(info["division"], inserted_dict["division"])
                eq_(info["category"], inserted_dict["category"])
                eq_(inserted_dict["is_deleted"], False)

    def test_delete_old(self):
        now = datetime.now()
        with Session() as session:
            all_news = session.query(News).all()
            for news in all_news:
                news.last_confirmed = now - timedelta(days=2)
            session.commit()
        with Session() as session:
            all_news = session.query(News).filter(News.last_confirmed < now).all()
            for news in all_news:
                news.is_deleted = True
            session.commit()
        with Session() as session:
            all_news = session.query(News).all()
            for news in all_news:
                ok_(news.is_deleted)

    @raises(IntegrityError)
    def test_unique_key_error(self):
        with Session() as session:
            session.add(News(**NEWS_MODEL_DATA_DICTS[0]))
            session.commit()

    def test_update(self):
        update = News(**NEWS_MODEL_DATA_DICTS[0])
        now = datetime.now()
        with Session() as session:
            exist = session.query(News).filter_by(unique_hash=update.unique_hash).first()  # type: News
            exist.last_confirmed = now
            session.commit()
        with Session() as session:
            updated = session.query(News).filter_by(unique_hash=update.unique_hash).first()  # type: News
            eq_(now, updated.last_confirmed)

    def test_tweet_text_count(self):
        with Session() as session:
            all_news = session.query(News).all()
            for news in all_news:
                ok_(len(news.tweet_text) <= 140)
