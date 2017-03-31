import re
from typing import Union, List
from logging import getLogger
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
    logger = getLogger("ScrapeFunction")
    info_list = []
    # Select model
    scraped_class, model = classification_models(html.url)
    targets = find_all_tr(html) if model is not News else find_all_dl(html)
    for target in targets:
        if target is not None:
            target_msgs = target.find_all('td') if model is not News else target.find_all('dd')
            # create instances
            m = model(**scraped_class(target_msgs).__dict__)
            info_list.append(m)
    logger.debug("Scraping {url} ... [finished]".format(url=html.url))
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
    return bs.findAll('tr', attrs={'class': re.compile('^gen_')})


def find_all_dl(res: Response) -> list:
    """
    「お知らせ」一覧からdlタグの中身をパースする関数
    Args:
        res: requests.models.Response object
    Returns:
        <dl>タグの中身のリスト
    """
    bs = BeautifulSoup(res.text, "lxml")
    all_dl = bs.findAll("dl", attrs={'class': 'notice_list_dl'})
    return [target for target in all_dl if is_news_row(target.attrs["class"])]


def is_news_row(class_names: list) -> bool:
    regex = re.compile("(cat|div)")
    bool_list = [re.match(regex, class_name) for class_name in class_names]
    for match in bool_list:
        if match:
            return True
    return False
