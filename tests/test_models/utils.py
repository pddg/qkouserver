from sqlalchemy.inspection import inspect
from typing import Union, List, Callable

from qkoubot.models import Session, Info, Cancel, News

T = Union[Info, Cancel, News]
ARGS = Union[str, int]


def query_to_dict(result) -> dict:
    """
    Convert to dict from given model object such as models.Subject or models.Info and so on.
    Args:
        result: Subject, Info, Cancel, News object which was got by query
    Returns:
        Dictionary of given objects property.
    """
    res = {}
    instance = inspect(result)
    for key, obj in instance.attrs.items():
        if key != "id":
            res[key] = obj.value
    return res


def insert_all(model: Callable[[ARGS], T], data_list: List[dict]) -> bool:
    """
    Insert test data based on given model.
    Args:
        model: Info, News, Cancel, Subject model
        data_list: list of dict of data
    Returns:
        success is True, fail is False
    """
    try:
        with Session() as session:
            insert = [model(**data_dict) for data_dict in data_list]
            session.add_all(insert)
            session.commit()
        return True
    except Exception:
        return False


def delete_all(model: T) -> bool:
    """
    Delete test data based on given model.
    Args:
        model: Info, News, Cancel, Subject model
    Returns:
        success is True, fail is False
    """
    try:
        with Session() as session:
            exists = session.query(model).all()
            for exist in exists:
                session.delete(exist)
            session.commit()
        return True
    except Exception:
        return False
