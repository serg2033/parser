import requests
import csv

from bs4 import BeautifulSoup


class Parser:

    def __init__(self):
        self.url = "https://books.toscrape.com"
        self.url_short = "https://books.toscrape.com/"
        self.book_info = []
        self.links = []

    @staticmethod
    def get_page(url):
        """Method return an html or error message"""
        request = requests.get(url)
        if request.status_code == 200:
            return request.text
        else:
            return 'Error'

    def get_data(self):
        """Scraping and collect title, image link, price and status of books"""
        soup = BeautifulSoup(self.get_page(self.url), "lxml")
        # print(soup)

        books = soup.find("section").find("ol", class_="row").find_all("li")
        # print(len(books)) # 20
        # print(type(books)) # soup object
        for book in books:
            title = book.find("h3").find("a").get("title")
            image = f'{self.url_short}{book.find("img").get("src")}'
            price = book.find("p", class_="price_color").text.replace("Â", "")
            status = book.find("p", class_="instock availability").text.strip()
            link = f'{self.url_short}{book.find("h3").find("a").get("href")}'

            book_dict = {
                "title": title,
                "image": image,
                "price": price,
                "status": status,
                "link": link
            }

            self.book_info.append(book_dict)
            self.links.append(link)

            self.write_to_csv(book_dict)

        # print(len(self.book_info))
        # print(len(self.links))

    @staticmethod
    def write_to_csv(data):
        with open("data.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    data['title'],
                    data['image'],
                    data['price'],
                    data['status'],
                    data['link']
                )
            )



if __name__ == '__main__':
    parser = Parser()
    parser.get_data()
