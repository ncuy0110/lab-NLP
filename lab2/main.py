import bs4
import xlsxwriter

from urllib.request import Request, urlopen

from post import Post


def crawl_on_page(page_number):
    try:
        url = "https://viblo.asia/newest?page=" + str(page_number)
        req = Request(
            url=url,
            headers={'User-Agent': 'XYZ/5.0'}
        )
        webpage = urlopen(req).read()
        soup = bs4.BeautifulSoup(webpage, 'html.parser')

        posts = []
        for post in soup.find_all(class_="post-feed-item"):
            p = Post(post=post)
            posts.append(p)
            print(p.title)
        return posts
    except:
        return []


def main():
    page = 1
    records = 0
    posts = []
    while (records < 1000):
        new_crawl = crawl_on_page(page_number=page)
        page += 1
        records += len(new_crawl)
        posts += new_crawl

    with xlsxwriter.Workbook('result.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        worksheet.write_row(
            0, 0, ["Owner", "Title", "Categories", "Reading time(minutes)", "Content"])
        for row_num, post in enumerate(posts):
            worksheet.write_row(row_num+1, 0, post.to_array())


if __name__ == "__main__":
    main()
