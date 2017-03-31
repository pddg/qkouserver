from unicodedata import normalize


class NewsScraper(object):
    """
    Scrape news page.
    """
    def __init__(self, args):
        """
        args[0] -> 掲載日
        args[1] -> 発信元
        args[2] -> カテゴリ
        args[3] -> 掲載内容

        Args:
             args: 取得した<dl>タグの中身をnormalizeしたりした値のリスト
        """
        str_args = [normalize("NFKC", dl.text.strip()) for dl in args[0:4]]
        self.first = str_args[0]
        self.detail = str_args[3]
        self.link = self.find_link(args[3])
        self.division = str_args[1]
        self.category = str_args[2]

    @staticmethod
    def find_link(detail) -> str:
        # find URL in target text
        link_txt = ""
        if detail.a is not None:
            links = []
            for a in detail.find_all('a'):
                links.append(a.get('href'))
            link_txt = " ".join(links)
        return link_txt
