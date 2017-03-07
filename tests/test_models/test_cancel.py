import unittest
from datetime import datetime, timedelta
from nose.tools import eq_, raises, ok_
from sqlalchemy.exc import IntegrityError

from qkoubot.models import Cancel, Session, Base, engine
from .utils import insert_all, delete_all, query_to_dict
from static import CANCEL_MODEL_DATA_DICTS


class TestCancelModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        ok_(insert_all(Cancel, CANCEL_MODEL_DATA_DICTS))

    def tearDown(self):
        delete_all(Cancel)

    def doCleanups(self):
        delete_all(Cancel)

    def test_inserted_data_is_correct(self):
        with Session() as session:
            for cancel in CANCEL_MODEL_DATA_DICTS:
                inserted = session.query(Cancel).filter(Cancel.unique_hash == Cancel(**cancel).unique_hash).one()
                inserted_dict = query_to_dict(inserted)
                eq_(cancel["title"], inserted_dict["title"])
                eq_(cancel["teacher"], inserted_dict["teacher"])
                eq_(cancel["abstract"], inserted_dict["abstract"])
                eq_(cancel["period"], inserted_dict["period"])
                eq_(cancel["week"], inserted_dict["week"])
                eq_(datetime.strptime(cancel["day"], "%Y/%m/%d"), inserted_dict["day"])
                eq_(inserted_dict["is_deleted"], False)

    def test_delete_old(self):
        now = datetime.now()
        with Session() as session:
            all_cancel = session.query(Cancel).all()
            for cancel in all_cancel:
                cancel.last_confirmed = now - timedelta(days=2)
            session.commit()
        with Session() as session:
            all_cancel = session.query(Cancel).filter(Cancel.last_confirmed < now).all()
            for cancel in all_cancel:
                cancel.is_deleted = True
            session.commit()
        with Session() as session:
            all_cancel = session.query(Cancel).all()
            for cancel in all_cancel:
                ok_(cancel.is_deleted)

    @raises(IntegrityError)
    def test_unique_key_error(self):
        with Session() as session:
            session.add(Cancel(**CANCEL_MODEL_DATA_DICTS[0]))
            session.commit()

    def test_update(self):
        update = Cancel(**CANCEL_MODEL_DATA_DICTS[0])
        now = datetime.now()
        with Session() as session:
            exist = session.query(Cancel).filter_by(unique_hash=update.unique_hash).first()  # type: Cancel
            exist.last_confirmed = now
            session.commit()
        with Session() as session:
            updated = session.query(Cancel).filter_by(unique_hash=update.unique_hash).first()  # type: Cancel
            eq_(now, updated.last_confirmed)

    def test_tweet_text_count(self):
        with Session() as session:
            all_cancel = session.query(Cancel).all()
            for cancel in all_cancel:
                ok_(len(cancel.tweet_text) <= 140)
