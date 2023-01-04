import requests
import json
from bs4 import BeautifulSoup

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

response = requests.get('https://100nout.by/product-category/kompjuternaja-tehnika/noutbuki/?proizvoditel=dell,lenovo&tip=biznes&razr=fhd-1920x1080&tech=ips',
headers=headers).text

soup = BeautifulSoup(response, 'lxml')

arr = []

items = soup.find_all('li', class_='catalog__list-item')

for item in items:
    link = item.find('a', class_='p-card__pic').get('href')
    title = item.find('a', class_='p-card__info-more-title').text.strip()
    info = item.find('div', class_='p-card__info-more-short-desc')
    for p in info:
        pass
         
        
    sale_price = item.find('div', class_='salep sale__price').text
    price_value = item.find('span', class_='p-card__price-value').text
    # print(sale_price)

    book = dict(
        link = link,
        title = title,
        # param = param,
        sale_price = sale_price,
        price_value = price_value,
    )
    arr.append(book)

    with open('books.json', 'w', encoding='utf-8')  as f:
        json.dump(arr, f, ensure_ascii=False, indent=4)