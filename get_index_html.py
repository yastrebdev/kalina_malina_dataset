import requests
from fake_useragent import UserAgent

ua = UserAgent().random


def get_html(*, url, headers):
    res = requests.get(url=url, headers=headers)
    src = res.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)


if __name__ == '__main__':
    get_html(
        url = 'https://kalina-malina.ru/',
        headers = {
            'Accept': '*/*',
            'User-Agent': ua
        }
    )