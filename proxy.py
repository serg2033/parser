import requests
import random

from bs4 import BeautifulSoup


def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text

    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', class_='table table-striped table-bordered').find_all('tr')[1:21]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        proxy = {
            'schema': schema,
            'address': ip + ':' + port
        }
        proxies.append(proxy)

    return random.choice(proxies)


def get_html(url):
    # proxies = {'http': 'ipaddress:5000'}

    p = get_proxy()  # {'schema': '', 'address': ''}
    proxy = {p['schema']: p['address']}

    r = requests.get(url, proxies=proxy, timeout=5)
    # return r.text
    return r.json()['origin']


def main():
    # url = 'https://free-proxy-list.net/'
    print(get_proxy())

    # url = 'https://httpbin.org/ip'
    # print(get_html(url))


if __name__ == '__main__':
    main()
