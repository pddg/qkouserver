from unicodedata import normalize


class CancelScraper(object):
    """
    Scrape lecture cancellation page.
    """
    def __init__(self, args):
        """
        args[0] -> ID
        args[1] -> 学部
        args[2] -> 講義名
        args[3] -> 講師名
        args[4] -> 休講日
        args[5] -> 曜日
        args[6] -> 時限
        args[7] -> 概要
        args[8] -> 初回掲載日

        Args:
             args: 取得した<td>タグの中身をnormalizeしたりした値のリスト
        """
        str_args = [td.text.strip() for td in args[2:9]]
        self.title = normalize("NFKC", str_args[0])
        self.teacher = normalize("NFKC", str_args[1])
        self.day = normalize("NFKC", str_args[2])
        self.week = normalize("NFKC", str_args[3])
        self.period = normalize("NFKC", str_args[4])
        self.abstract = str_args[5] + self.find_link(args[7])
        self.first = normalize("NFKC", str_args[6])

    @staticmethod
    def find_link(detail) -> str:
        """
        find URL in target text

        Args:
            detail: BeautifulSoup object

        Returns:
            Link text string.
        """
        link_txt = ""
        if detail.a is not None:
            links = []
            for a in detail.find_all('a'):
                links.append(a.get('href'))
            link_txt = " ".join(links)
        return link_txt
