import requests
from bs4 import BeautifulSoup
import os
import sys
import re
import traceback


def make_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return f"Error {response.status_code}"


def get_links(html):
    links = []
    soup = BeautifulSoup(html, "lxml")

    trash = soup.find_all("div", class_=re.compile("news-entry"))
    for i in trash:
        link = i.find("a").get("href")
        links.append(link)
    return links


def parse_news(url):
    dir_name = url.split("/")[-2].capitalize()
    data = []
    soup = BeautifulSoup(make_request(url), "lxml")
    category = soup.find("a", itemprop="articleSection").text.strip()
    file_name = soup.find("h1").text.replace("\xa0", " ").split(".")[0]
    header = soup.find("h1").text.replace("\xa0", " ")
    date_, time_ = soup.find("time").get("datetime").split("T")
    time = time_.split("+")[0]
    text = soup.find("div", id="article_body").text.strip().replace("\xa0", " ")
    data.append(
        category + "\n\n" + header + "\n\n" + date_ + "\t" + time + "\n\n" + text
    )

    if not os.path.exists(f"{date}/{dir_name}"):
        os.mkdir(f"{date}/{dir_name}")

    write_into_file(dir_name, file_name, *data)


def write_into_file(dir_name, name, data):
    with open(f"{date}/{dir_name}/{name}.txt", "w") as file:
        file.write(data)


date = sys.argv[1]

if not os.path.exists(date):
    os.mkdir(date)


links = get_links(make_request(f"https://news.zerkalo.io/archive/{date}.html"))
count = 1
for link in links:
    try:
        parse_news(link)
        print(f"спарсил {count} новостей")
        count += 1
    except:
        traceback.print_exc()
        print("skip")
