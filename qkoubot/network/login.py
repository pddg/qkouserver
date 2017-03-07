from logging import Logger
from typing import List

from requests.models import Response

from static import LEC_INFO_URL, LEC_CANCEL_URL, NEWS_URL, SHIBBOLETH_USERNAME, SHIBBOLETH_PASSWORD
from .shibboleth_login import ShibbolethClient


async def get_html(br, url) -> Response:
    return br.get(url)


async def login_and_get_html(logger: Logger) -> List[Response]:
    """
    This is an asynchronous function. Get html from website.
    Args:
        logger: logging.Logger object.
    Returns:
        List of requests.models.Response include html string.
    """
    urls = [NEWS_URL, LEC_INFO_URL, LEC_CANCEL_URL]
    br = ShibbolethClient(SHIBBOLETH_USERNAME, SHIBBOLETH_PASSWORD)
    with br:
        logger.debug("Login Succeeded and try to get information...")
        obj_list = []
        for u in urls:
            r = await get_html(br, u)
            logger.debug("[{url}] finished".format(url=r.url))
            obj_list.append(r)
    return obj_list
