from unicodedata import normalize


class NewsScraper(object):
    """
    Scrape news page.
    """
    def __init__(self, args):
        """
        args[0] -> 掲載日
        args[1] -> 掲載内容

        Args:
             args: 取得した<td>タグの中身をnormalizeしたりした値のリスト
        """
        str_args = [td.text.strip() for td in args[0:2]]
        self.first = normalize("NFKC", str_args[0])
        self.detail = str_args[1]
        self.link = self.find_link(args[1])

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
