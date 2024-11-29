import requests
from fake_useragent import UserAgent

import random
from time import sleep

import json
import csv

ua = UserAgent().random

headers = {
    'User-Agent': ua,
    'Accept': 'application/json'
}

with open('urls/category_urls.csv', 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        url = row[1]

        res = requests.get(url = url, headers = headers)
        data = json.loads(res.text)
        sub_categories = data['childs']

        for sub_category in sub_categories:
            products = sub_category['products']

            for product in products:
                product_id = product['id']
                product_url = f'https://admin.kalina-malina.ru/api/v1/products/{product['slug']}'

                with open('urls/product_urls.csv', 'a', encoding='utf-8', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([product_id, product_url])

        sleep(random.randrange(2, 4))