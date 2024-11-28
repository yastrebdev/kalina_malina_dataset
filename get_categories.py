from idlelib.iomenu import encoding

import requests
from fake_useragent import UserAgent

import json
import csv

ua = UserAgent().random

headers = {
    'User-Agent': ua,
    'Accept': 'application/json'
}

with open('urls/sub_categories.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)

    with open('data/categories.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['id', 'name','slug'])

    for row in reader:
        url = row[1]

        res = requests.get(url=url, headers=headers)
        data = json.loads(res.text)

        category = data['category']

        category_id = category['id']
        category_name = category['title']
        category_slug = category['slug']

        with open('data/categories.csv', 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([category_id, category_name, category_slug])