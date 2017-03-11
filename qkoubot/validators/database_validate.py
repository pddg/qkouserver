import os
from static import SQLITE_DIR_PATH, USE_MYSQL, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASE_NAME


def db_path_validate():
    assert os.path.exists(SQLITE_DIR_PATH), "{path} is not exists.".format(path=SQLITE_DIR_PATH)
    if USE_MYSQL:
        assert MYSQL_USERNAME is not None, "MYSQL_USERNAME is not given."
        assert MYSQL_PASSWORD is not None, "MYSQL_PASSWORD is not given."
        assert MYSQL_HOST is not None, "MYSQL_HOST is not given."
        assert MYSQL_DATABASE_NAME is not None, "MYSQL_DATABASE_NAME is not given."
