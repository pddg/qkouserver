from logging import getLogger

from qkoubot.models import Session, News, Info, Cancel
from static import THERE_IS_NO_INFORMATION_MSG, DATABASE_ERROR_MSG


class ReplyInfo(object):

    def __init__(self):
        self.model = Info
        self.session = Session
        self.logger = getLogger(__name__)

    def get_info_by_id(self, id_: int) -> str:
        """
        Get information from database, and return message.

        Args:
            id_: Data's primary key.
        Returns:
            Result message sending with DM.
        """
        try:
            with self.session() as session:
                info = session.query(self.model).filter(self.model.id == id_).first()
                self.logger.debug("Get data that id is {id} from database.".format(id=id_))
                return str(info) if info and not info.is_deleted else THERE_IS_NO_INFORMATION_MSG
        except Exception as e:
            self.logger.exception(e.args)
            return DATABASE_ERROR_MSG


class ReplyCancel(ReplyInfo):

    def __init__(self):
        super(ReplyCancel, self).__init__()
        self.model = Cancel


class ReplyNews(ReplyInfo):

    def __init__(self):
        super(ReplyNews, self).__init__()
        self.model = News
