from urllib.request import Request, urlopen
from bs4.element import Tag
import bs4


class Post:
    def __init__(self, post: Tag):
        self.owner = post.find(
            "span", class_="el-popover__reference-wrapper").get_text().strip()

        self.title = post.find(
            "div", class_="post-title--inline").h3.get_text().strip()

        self.categories = []
        for cat in post.find("div", class_="post-title--inline").div.find_all("a"):
            self.categories.append(cat.get_text().strip())

        self.reading_time = int(post.find(
            "span", class_="post-reading_time mr-05 is-divide text-muted").get_text().split()[0])

        content_url = "https://viblo.asia" + post.find(
            "div", class_="post-title--inline").h3.a.get("href")

        self.content = self.crawl_content(content_url)

    def crawl_content(self, content_url):
        req = Request(
            url=content_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        webpage = urlopen(req).read()
        soup = bs4.BeautifulSoup(webpage, 'html.parser')

        return soup.find("div", "md-contents").get_text()

    def to_array(self):
        return [self.owner, self.title, ", ".join(self.categories), self.reading_time, self.content]
