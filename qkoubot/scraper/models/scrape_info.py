from unicodedata import normalize


class InfoScraper(object):
    """
    授業関係連絡のページから取得したHTMLをパース．取得したtrタグの中身をさらにパースしてプロパティにする．
    """
    def __init__(self, args):
        """
        args[0] -> ID
        args[1] -> 学部
        args[2] -> セメスター
        args[3] -> 講義名
        args[4] -> 講師名
        args[5] -> 曜日
        args[6] -> 時限
        args[7] -> 概要
        args[8] -> 詳細
        args[9] -> 初回掲載日
        args[10] -> 最終更新日

        Args:
             args: 取得した<td>タグの中身をnormalizeしたりした値のリスト
        """
        str_args = [td.text.strip() for td in args[3:]]
        self.title = normalize("NFKC", str_args[0])
        self.teacher = normalize("NFKC", str_args[1])
        week_raw = normalize("NFKC", str_args[2])
        self.week = week_raw[0] if "曜日" in week_raw else week_raw
        self.period = normalize("NFKC", str_args[3])
        self.abstract = normalize("NFKC", str_args[4])
        self.detail = str_args[5] + " " + self.find_link(args[5])
        self.first = normalize("NFKC", str_args[6])
        self.updated_date = normalize("NFKC", str_args[7])

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
