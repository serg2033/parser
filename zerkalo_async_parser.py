import aiohttp
import asyncio
from bs4 import BeautifulSoup
import requests
import re
import os
import sys
import traceback
import time


date = sys.argv[1]

page = 0

if not os.path.exists(date):
    os.mkdir(date)


async def get_page(session, url):
    # get data(html) from page
    async with session.get(url) as response:
        return await response.text()


async def get_all(session, urls):
    # pull tasks together
    tasks = []
    for url in urls:
        task = asyncio.create_task(get_page(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main(urls):
    # control function
    async with aiohttp.ClientSession() as session:
        data = await get_all(session, urls)
    return data


def parse(results):
    # parse page
    for html in results:
        soup = BeautifulSoup(html, "lxml")
        try:
            category = soup.find("a", itemprop="articleSection").text.strip()
            file_name = soup.find("h1").text.replace("\xa0", " ").split(".")[0]
            header = soup.find("h1").text.replace("\xa0", " ")
            date_, time_ = soup.find("time").get("datetime").split("T")
            time = time_.split("+")[0]
            text = soup.find("div", id="article_body").text.strip().replace("\xa0", " ")

            if not os.path.exists(f"{date}/{category}/"):
                os.mkdir(f"{date}/{category}/")

            with open(f"{date}/{category}/{file_name}.txt", "w") as file:
                file.write(
                    category
                    + "\n\n"
                    + header
                    + "\n\n"
                    + date_
                    + "\t"
                    + time
                    + "\n\n"
                    + text
                )
            global page
            print(f"scraping {page}")
            page += 1

        except:
            traceback.print_exc()
            print("skip")


def get_links(url):
    # collect links from page
    response = requests.get(url).text
    soup = BeautifulSoup(response, "lxml")
    links = []
    trash = soup.find_all("div", class_=re.compile("news-entry"))
    for i in trash:
        link = i.find("a").get("href")
        links.append(link)
    return links


if __name__ == "__main__":
    start = time.perf_counter()

    urls = get_links(f"https://news.zerkalo.io/archive/{date}.html")

    results = asyncio.run(main(urls))
    parse(results)
    print(time.perf_counter() - start)

