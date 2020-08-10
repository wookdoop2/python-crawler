from itertools import count
import pandas as pd

from bs4 import BeautifulSoup

from collection import crawler


def crawling_pelicana():
    # result = list()
    result = []

    for page in count(start=1, step=1):
        url = "https://pelicana.co.kr/store/stroe_search.html?page=%d&branch_name=&gu=&si=" % page
        html = crawler.crawling(url)
        # print(html)

        bs = BeautifulSoup(html, "html.parser")
        tag_table = bs.find("table", attrs={"class": ["table", "mt20"]})
        tag_tbody = tag_table.find("tbody")
        tags_tr = tag_tbody.findAll("tr")
        # print(tags_tr)

        # 끝 검출 (tbody empty)
        if len(tags_tr) == 0:
            break

        # text만 따로 list로 담아준다
        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print(strings)

            name = strings[1]
            address = strings[3]
            # print(name, address, sep=":")

            sidogu = address.split()[0:2]
            # print(sidogu)
            t = (name, address) + tuple(sidogu)
            result.append(t)

    print(result)

    # store
    table = pd.DataFrame(result, columns=["name", "address", "sido", "gigun"])
    table.to_csv("results/pelicana.csv", encoding="utf-8", mode="w", index=True)


def crawling_kyochon():
    pass


def crawling_goobne():
    print("crawling_goobne")


if __name__ == "__main__":
    # pelicana
    crawling_pelicana()

    # nene

    # kyochon

    # goobne
