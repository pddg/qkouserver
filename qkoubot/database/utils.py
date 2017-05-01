from datetime import datetime, timedelta
from typing import Union, Type
from sqlalchemy.exc import IntegrityError
from logging import getLogger

from qkoubot.models import Session, Info, Cancel, News

T = Union[Info, Cancel, News]


def add(data: T) -> bool:
    """
    Add to database.

    Args:
        data: Info or Cancel or News or Subject model

    Returns:
        If True, adding to DB is success. If False, unique key error occurs.
    """
    try:
        with Session() as sess:
            sess.add(data)
            sess.commit()
            return True
    except IntegrityError:
        # unique key error
        # new data and existence data in DB are duplicates.
        with Session() as sess:
            if isinstance(data, Info):
                return False
            exists = sess.query(data.__class__).filter_by(unique_hash=data.unique_hash).first()  # type: T
            exists.last_confirmed = data.last_confirmed
            sess.commit()
        return False


def update_info(data: Info) -> bool:
    """
    Update database with given data.

    Args:
        data: Info model

    Returns:
        When success, return True. If there is no need to update, return False.
    """
    logger = getLogger("update")
    with Session() as sess:
        exist = sess.query(Info).filter(
            Info.unique_hash == data.unique_hash).first()  # type: Info
        if exist.renew_hash != data.renew_hash:
            if (data.last_confirmed - exist.last_confirmed).total_seconds() < 5:
                logger.debug("[IGNORE] " + data.__repr__())
                # 暫定処理として同一の主キーとなるに関わらず，内容が変化している項目が複数掲載された場合，変更を握りつぶす．
                return False
            # Update data
            data.id = exist.id
            exist.detail = data.detail
            exist.updated_date = data.updated_date
            exist.renew_hash = data.renew_hash
            exist.last_confirmed = datetime.now()
            sess.commit()
            return data.id
        else:
            # There is no update.
            exist.last_confirmed = datetime.now()
            sess.commit()
            return False


def delete_olds(table: Type[T]) -> bool:
    """
    Delete data created at 1day or more old.

    Args:
        table: Info or Cancel or News model

    Returns:
        When success, return True. If there is no old information, return False.
    """
    logger = getLogger("DeleteOld")
    with Session() as session:
        yday = datetime.now() - timedelta(days=1)
        logger.debug("Delete '{table}' data confirmed finally more than '{date}' before"
                     .format(table=table.__tablename__, date=yday.strftime("%Y/%m/%d %H:%M")))
        olds = [old for old in session.query(table).filter(table.last_confirmed < yday).all() if not old.is_deleted]
        if len(olds) == 0:
            return False
        for old in olds:
            logger.debug("[DELETE] " + old.__repr__())
            old.is_deleted = True
        session.commit()
        return True
