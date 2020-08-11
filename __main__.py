import time
from datetime import datetime
from itertools import count
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver

from collection import crawler


def crawling_nene():
    result = []
    for page in range(1, 48):
        url = "https://nenechicken.com/17_new/sub_shop01.asp?page=%d&ex_select=1&ex_select2=&IndexSword=&GUBUN=A" % page
        html = crawler.crawling(url)
        # print(html)

        bs = BeautifulSoup(html, "html.parser")
        tag_div = bs.find("div", attrs={"class": "shopWrap"})
        tags_div0 = tag_div.findAll("div", attrs={"class": "shopName"})
        tags_div1 = tag_div.findAll("div", attrs={"class": "shopAdd"})

        for i in range(0, len(tags_div0)):
            strings0 = list(tags_div0[i].strings)
            strings1 = list(tags_div1[i].strings)

            t = (strings0[0], strings1[0]) + tuple(strings1[0].split()[0:2])
            result.append(t)

    print(result)

    # store
    table = pd.DataFrame(result, columns=["name", "address", "sido", "gigun"])
    table.to_csv("results/nene.csv", encoding="utf-8", mode="w", index=True)


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
    table.to_csv("results/pelicana.csv", encoding="UTF-8", mode="w", index=True)


def crawling_kyochon():
    result = []
    for sido1 in range(1, 18):
        for sido2 in count(start=1, step=1):
            url = "http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=" % (sido1, sido2)
            html = crawler.crawling(url)
            # print(html)

            if html is None:
                break

            bs = BeautifulSoup(html, "html.parser")
            tag_ul = bs.find("ul", attrs={"class": "list"})
            tags_span = tag_ul.findAll("span", attrs={"class": "store_item"})

            for tag_span in tags_span:
                strings = list(tag_span.strings)
                # print(strings)

                name = strings[1];
                address = strings[3].strip("\r\n\t")

                sidogu = address.split()[0:2]
                t = (name, address) + tuple(sidogu)
                # print(t)
                result.append(t)
    print(result)

    # store
    table = pd.DataFrame(result, columns=["name", "address", "sido", "gigun"])
    table.to_csv("results/kyochon.csv", encoding="utf-8", mode="w", index=True)


def crawling_goobne():
    url = "https://www.goobne.co.kr/store/search_store.jsp"

    # 첫 페이지 로딩
    wd = webdriver.Chrome("C:\\bit2020\\chromedriver_win32\\chromedriver.exe")
    wd.get(url)
    time.sleep(3)

    # Javascript 실행
    script = "store.getList(1)"
    wd.execute_script(script)
    print(f"{datetime.now()} : success for request[{script}]")
    time.sleep(2)

    # Javascript 실행 결과 HTML(동적으로 rendering 된 HTML) 가져오기
    html = wd.page_source
    print(html)


if __name__ == "__main__":
    # pelicana
    # crawling_pelicana()

    # nene (assignment)
    # crawling_nene()

    # kyochon
    # crawling_kyochon()

    # goobne
    crawling_goobne()