import requests
import csv

from bs4 import BeautifulSoup


url = "https://books.toscrape.com/catalogue/page-1.html"


def get_html(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    print(f"error {r.status_code}")


def get_page(html):
    soup = BeautifulSoup(get_html(url), "lxml")

    books = soup.find("section").find("ol", class_="row").find_all("li")
    for book in books:
        title = book.find("h3").find("a").get("title")
        # print(title)
        image = f'{"https://books.toscrape.com/"}{book.find("img").get("src")}'
        # print(image)
        price = book.find("p", class_="price_color").text.replace("Â", "")
        # print(price)
        status = book.find("p", class_="instock availability").text.strip()
        # print(status)
        link = f'{"https://books.toscrape.com/catalogue/"}{book.find("h3").find("a").get("href")}'
        # print(link)

        soup2 = BeautifulSoup(get_html(link), "lxml")
        desc = soup2.find("div", class_="sub-header").find_next().find_next().text

        # print(desc)

        book_dict = {
            "title": title,
            "image": image,
            "price": price,
            "status": status,
            "link": link,
            "desc": desc,
        }
        write_to_csv(book_dict)


def write_to_csv(data):
    with open("datafull.csv", "a", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                data["title"],
                data["image"],
                data["price"],
                data["status"],
                data["link"],
                data["desc"],
            )
        )


def get_next_page(html):
    soup = BeautifulSoup(html, "lxml")
    try:
        next_page = "https://books.toscrape.com/catalogue/" + soup.find(
            "li", class_="next"
        ).find("a").get("href")
        return next_page
    except:
        pass


def main():
    # get_page(get_html(url))
    # print(get_next_page(get_html(url)))
    page = 1

    url = "https://books.toscrape.com/catalogue/page-1.html"
    while True:
        print(page)
        get_page(get_html(url))

        soup = BeautifulSoup(get_html(url), "lxml")

        try:
            url = "https://books.toscrape.com/catalogue/" + soup.find(
                "li", class_="next"
            ).find("a").get("href")
            page += 1
        except:
            break


if __name__ == "__main__":
    main()
