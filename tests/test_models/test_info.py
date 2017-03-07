import unittest
from datetime import datetime, timedelta
from nose.tools import eq_, raises, ok_, assert_not_equal as neq_
from sqlalchemy.exc import IntegrityError

from qkoubot.models import Info, Session, Base, engine
from .utils import insert_all, delete_all, query_to_dict
from static import INFO_MODEL_DATA_DICTS, SUBJECT_MODEL_DATA_DICTS


class TestInfoModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(engine)

    def setUp(self):
        ok_(insert_all(Info, INFO_MODEL_DATA_DICTS))

    def tearDown(self):
        delete_all(Info)

    def doCleanups(self):
        delete_all(Info)

    def test_inserted_data_is_correct(self):
        with Session() as session:
            for info in INFO_MODEL_DATA_DICTS:
                inserted = session.query(Info).filter(Info.unique_hash == Info(**info).unique_hash).one()
                inserted_dict = query_to_dict(inserted)
                eq_(info["title"], inserted_dict["title"])
                eq_(info["teacher"], inserted_dict["teacher"])
                eq_(info["period"], inserted_dict["period"])
                eq_(info["week"], inserted_dict["week"])
                eq_(info["abstract"], inserted_dict["abstract"])
                eq_(info["detail"], inserted_dict["detail"])
                eq_(inserted_dict["is_deleted"], False)

    def test_delete_old(self):
        now = datetime.now()
        with Session() as session:
            all_info = session.query(Info).all()
            for info in all_info:
                info.last_confirmed = now - timedelta(days=2)
            session.commit()
        with Session() as session:
            all_info = session.query(Info).filter(Info.last_confirmed < now).all()
            for info in all_info:
                info.is_deleted = True
            session.commit()
        with Session() as session:
            all_info = session.query(Info).all()
            for info in all_info:
                ok_(info.is_deleted)

    @raises(IntegrityError)
    def test_unique_key_error(self):
        with Session() as session:
            session.add(Info(**INFO_MODEL_DATA_DICTS[0]))
            session.commit()

    def test_update(self):
        update_data = INFO_MODEL_DATA_DICTS[0]
        update_data["updated_date"] = "2017/2/25"
        update_data["detail"] = "上条ちゃんと土御門ちゃんは補習でーす"
        update = Info(**update_data)
        now = datetime.now()
        with Session() as session:
            exist = session.query(Info).filter_by(unique_hash=update.unique_hash).first()  # type: Info
            neq_(update.renew_hash, exist.renew_hash)
            exist.last_confirmed = now
            exist.detail = update.detail
            exist.renew_hash = update.renew_hash
            exist.updated_date = update.updated_date
            session.commit()
        with Session() as session:
            updated = session.query(Info).filter_by(unique_hash=update.unique_hash).first()  # type: Info
            eq_(update.renew_hash, updated.renew_hash)
            eq_(update.detail, updated.detail)
            eq_(update.updated_date, updated.updated_date)
            eq_(now, updated.last_confirmed)

    def test_tweet_text_count(self):
        with Session() as session:
            all_info = session.query(Info).all()
            for info in all_info:
                ok_(len(info.tweet_text) <= 140)
