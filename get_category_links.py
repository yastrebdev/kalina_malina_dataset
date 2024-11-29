from bs4 import BeautifulSoup
import csv

with open('index.html', 'r', encoding = 'utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

categories_menu = soup.find(class_ = 'hideScrollBar max-h-[calc(100dvh-350px)] overflow-auto px-3.75 md:max-h-[calc(100vh-155px)] max-md:pb-6')

category_links = categories_menu.find_all('a')

sub_categories = []
with open('urls/category_urls.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)

    rep = [', ', ' ']
    for link in category_links:
        text = link.text.replace('"', '')
        for char in rep:
            text = text.replace(char, '_')

        href = link.get('href')
        url = f'https://admin.kalina-malina.ru/api/v1/products{href}?storeOneCId=ae5b9239-4a60-11ef-98e2-005056ab1c52&limit=20'

        if href.count('/') >= 3:
            writer.writerow([text, url])
        else:
            sub_categories.append((text, url))

for category in sub_categories:
    with open('urls/sub_categories_urls.csv', 'a', encoding='utf-8', newline='') as c_f:
        writer = csv.writer(c_f)
        writer.writerow([category[0], category[1]])