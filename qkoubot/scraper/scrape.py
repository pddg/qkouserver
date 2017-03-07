import re
from typing import Union, List
from bs4 import BeautifulSoup
from requests.models import Response
from qkoubot.models import Info, News, Cancel
from .models import InfoScraper, CancelScraper, NewsScraper

DM = Union[Info, News, Cancel]


def scrape_process(html: Response) -> List[DM]:
    """
    This function provides the process of scraping from html sources and sort it.

    Args:
        html: requests.models.Response object

    Returns:
        List of Info and Cancel and News model's instance.
    """
    info_list = []
    # Select model
    scraped_class, model = classification_models(html.url)
    for tr in find_all_tr(html):
        if tr is not None:
            td = tr.find_all('td')
            # create instances
            m = model(**scraped_class(td).__dict__)
            info_list.append(m)
    return info_list


def classification_models(url: str):
    """
    classify by URL

    Args:
        url: url string

    Returns:
        Tuple of Scraper model and DB model.
    """
    if "lecture_information" in url:
        return InfoScraper, Info
    elif "lecture_cancellation" in url:
        return CancelScraper, Cancel
    else:
        return NewsScraper, News


def find_all_tr(res: Response) -> list:
    """
    This function find out all 'tr' tags in html and return list of them.

    Args:
        res: requests.models.Response object

    Returns:
        List of all <tr> tag which is in the target class.
    """
    # Use lxml as html parser.
    bs = BeautifulSoup(res.text, "lxml")
    if "info" in res.url or "cancel" in res.url:
        # ?c=lecture_information or ?c=lecture_cancellation
        return bs.find_all('tr', attrs={'class': re.compile('^gen_')})
    else:
        # ?c=news
        div = bs.find('div', attrs={'id': 'now_notice_area'})
        return div.find_all('tr')
