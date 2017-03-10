from datetime import datetime, timedelta
from typing import Union
from sqlalchemy import and_
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
        return False


def update_info(data: Info) -> bool:
    """
    Update database with given data.

    Args:
        data: Info model

    Returns:
        When success, return True. If there is no need to update, return False.
    """
    with Session() as sess:
        exist = sess.query(Info).filter(
            and_(Info.unique_hash == data.unique_hash, Info.is_deleted is not True)).first()  # type: Info
        if exist.renew_hash != data.renew_hash:
            # Update data
            data.subject = exist.subject
            exist.detail = data.detail
            exist.updated_date = data.updated_date
            exist.renew_hash = data.renew_hash
            exist.last_confirmed = datetime.now()
            sess.commit()
            return True
        else:
            # There is no update.
            return False


def delete_olds(table: T) -> bool:
    """
    Delete data created at 1day or more old.

    Args:
        table: Info or Cancel or News model

    Returns:
        When success, return True. If there is no old information, return False.
    """
    logger = getLogger("DeleteOld")
    with Session() as session:
        olds = session.query(table).filter(table.created_at < (datetime.now() - timedelta(days=1))).all()
        if len(olds) == 0:
            return False
        for old in [old for old in olds if not old.is_deleted]:
            logger.debug("[DELETE] " + str(old))
            old.is_deleted = True
        session.commit()
        return True
