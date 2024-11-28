import requests
from fake_useragent import UserAgent

import random
from time import sleep
from datetime import datetime

import json
import csv
import os

ua = UserAgent()

headers = {
    'User-Agent': ua.random,
    'Accept': 'application/json'
}

all_reviews = []
products = []

cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')

if not os.path.exists('data'):
    os.makedirs('data')


def write_csv_headers(file_path, headers):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        with open(file_path, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)


write_csv_headers(f'data/{cur_time}_products.csv', [
    'id', 'category_id', 'name', 'composition', 'rating', 'unit', 'cooking', 'priceUnit', 'price',
    'proteins', 'fats', 'carbohydrates', 'nutritionKcal', 'nutritionKj',
    'storageConditions', 'shelfLife', 'vegan', 'review_count'
])

write_csv_headers(f'data/{cur_time}_reviews.csv', [
    'id', 'product_id', 'rating', 'text', 'date', 'user_name'
])

try:
    with open('urls/product_urls.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        urls = list(reader)

    print(f'Количество продуктов: {len(urls)}')

    for count, row in enumerate(urls, start=1):
        try:
            if len(row) < 2:
                print(f'Пропущена строка #{count}: некорректный формат данных')
                continue

            url = row[1]
            res = requests.get(url=url, headers=headers)

            if res.status_code != 200:
                print(f"Ошибка запроса #{count}: {res.status_code} для URL {url}")
                continue

            data = res.json()

            product_id = data.get('id')
            category_id = data.get('categoryId', 0)
            name = data.get('title', 'Без названия')
            description = data.get('description', 'Нет описания')
            composition = data.get('composition', 'Не указано')
            rating = data.get('rating', 0)
            unit = data.get('unit', 'Не указано')
            cooking = data.get('cooking', 'Нет информации')
            priceUnit = data.get('priceUnit', 'Не указано')
            price = data.get('price', 0)

            images = []
            if data.get('images'):
                images = [img.get('image') for img in data.get('images', []) if img.get('image')]

            properties = data.get('properties', {})
            proteins = properties.get('proteins', 0)
            fats = properties.get('fats', 0)
            carbohydrates = properties.get('carbohydrates', 0)
            nutritionKcal = properties.get('nutritionKcal', 0)
            nutritionKj = properties.get('nutritionKj', 0)
            storage_conditions = properties.get('storageConditions', 'Не указано')
            shelf_life = properties.get('shelfLife', 'Не указано')
            vegan = properties.get('vegan', 0)
            review_count = data.get('reviewCount', 0)

            # Обработка отзывов
            reviews = []
            if review_count > 0:
                reviews_res = requests.get(url=f'{url}/review', headers=headers)

                if reviews_res.status_code == 200:
                    reviews_data = reviews_res.json()
                    for review in reviews_data:
                        reviews.append({
                            'id': review.get('id'),
                            'product_id': product_id,
                            'rating': review.get('rating', 0),
                            'text': review.get('text', 'Нет текста'),
                            'date': review.get('date', 'Не указана'),
                            'user_name': review.get('user', {}).get('firstName', 'Аноним')
                        })
                        all_reviews.append(reviews[-1])
                else:
                    print(f"Ошибка загрузки отзывов для продукта {product_id}: {reviews_res.status_code}")

            # Сохранение данных продукта
            products.append({
                'id': product_id,
                'category_id': category_id,
                'name': name,
                'description': description,
                'composition': composition,
                'rating': rating,
                'unit': unit,
                'cooking': cooking,
                'priceUnit': priceUnit,
                'price': price,
                'images': images,
                'properties': properties,
                'reviews': reviews,
                'review_count': review_count,
            })

            with open(f'data/{cur_time}_products.csv', 'a', encoding='utf-8', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([
                    product_id, category_id, name, composition, rating, unit, cooking, priceUnit, price,
                    proteins, fats, carbohydrates, nutritionKcal, nutritionKj,
                    storage_conditions, shelf_life, vegan, review_count
                ])

            with open(f'data/{cur_time}_reviews.csv', 'a', encoding='utf-8', newline='') as c_f:
                writer = csv.writer(c_f)
                for review in reviews:
                    writer.writerow([
                        review['id'], review['product_id'], review['rating'], review['text'], review['date'], review['user_name']
                    ])

            print(f'# Итерация {count}. {name} записан...')

            # Задержка между запросами
            sleep(random.uniform(1, 2))

        except Exception as e:
            print(f"Ошибка обработки продукта #{count}: {e}")

except Exception as e:
    print(f"Ошибка работы с файлом product_urls.csv: {e}")

# Сохранение итоговых данных в JSON
try:
    with open(f'data/{cur_time}_products.json', 'w', encoding='utf-8') as json_file:
        json.dump(products, json_file, indent=4, ensure_ascii=False)

    with open(f'data/{cur_time}_reviews.json', 'w', encoding='utf-8') as j_f:
        json.dump(all_reviews, j_f, indent=4, ensure_ascii=False)

except Exception as e:
    print(f"Ошибка записи JSON файлов: {e}")