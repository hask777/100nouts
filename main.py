import requests
import json
from bs4 import BeautifulSoup

def get_books():

    url = 'https://100nout.by/product-category/kompjuternaja-tehnika/noutbuki/?proizvoditel=lenovo'

    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}

    response = requests.get(url,
    headers=headers).text

    soup = BeautifulSoup(response, 'lxml')

    pages = soup.find('ul', class_='page-numbers')
    pages = pages.find_all('li')
    last_page = pages[-2].text

    arr = []
    count = 0

    for page in range(1, int(last_page)+1):
    
        url = f'https://100nout.by/product-category/kompjuternaja-tehnika/noutbuki/page/{page}/?proizvoditel=lenovo'

        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
        response = requests.get(url,
        headers=headers).text
        # print(url)

        soup = BeautifulSoup(response, 'lxml')
        items = soup.find_all('li', class_='catalog__list-item')

        for item in items:
            link = item.find('a', class_='p-card__pic').get('href')
            title = item.find('a', class_='p-card__info-more-title').text.replace('\n', '').strip()
            info = item.find('div', class_='p-card__info-more-short-desc').find_all('p')
            
            params = []
            # print(info)
            for s in info:
                s = s.find_all('span')
                for i in s:
                    name = s[0].text
                    value = s[1].text
                        
                params.append( dict(
                    name = name.strip(),
                    value = value.strip()
                ))       

            sale_price = item.find('div', class_='salep sale__price').text
            price_value = item.find('span', class_='p-card__price-value').text
            count += 1

            book = dict(
                link = link,
                title = title,
                params = params,
                sale_price = sale_price,
                price_value = price_value,
                count = count
            )

            arr.append(book)
            # print(len(arr))
            
        arr.append(dict(total = count))

    with open('books.json', 'w', encoding='utf-8')  as f:
        json.dump(arr, f, ensure_ascii=False, indent=4)

def main():
    get_books()


if __name__ == '__main__':
    main()