import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()

list_cat_url = []
count = 0
carts = []

url = "https://stroydomsale.ru/catalog"
headers = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}

req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('div', class_="category--tree")
for item in list_catigories_1lv:
    item = item.find('a').get('href')
    list_cat_url.append({
        'url_cat': f"https://stroydomsale.ru{item}",
    })

# Цикл для перехода по разделам
for item in tqdm(list_cat_url):
    req = requests.get(item['url_cat'], headers=headers)
    soup = BeautifulSoup(req.text, "lxml")


    count += 1
    print(f"Обработка {count} каталога ")

    if soup.find("ul", class_="pager__items"):
        # найти последнее значение в пагинации
        if (soup.find("ul", class_="pager__items").find_all("span", class_="pager-item-label")[-1].text) == "":
            pages_count = int(soup.find("ul", class_="pager__items").find_all("span", class_="pager-item-label")[-2].text)
        else:
            pages_count = int(soup.find("ul", class_="pager__items").find_all("span", class_="pager-item-label")[-1].text)

        # цикл по пагинации
        for i in range(0, pages_count):
            if i == 0:
                url_page = item['url_cat']
            else:
                url_page = f"{item['url_cat']}?page={i}"


            req = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(req.text, "lxml")

            print(url_page)
            link_products_list = soup.find('div', class_='view-content').find_all('div', 'views-row')
            for item_cart in link_products_list:
                try:
                    url = "https://stroydomsale.ru" + item_cart.find('a').get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('h3').getText()
                except Exception:
                    name = 'none'
                try:
                    price = item_cart.find('span', class_="price-value").getText()
                except Exception:
                    price = 'none'  # Цены нет, если нет в наличие

                carts.append({
                    "url": f"{url}",
                    "name": name,
                    "price": price,
                })

    # # print(carts)
with open("/Users/artem/Desktop/parser_stroyoz-master/resul_parce/stroydomsale.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)
print("--- %s seconds ---" % (time.time() - start_time))