import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

carts = []

list_cat_url = []
count = 0

url = "http://dvoroz.ru/sitemap_tovar.xml"
headers ={
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
req = requests.get(url, headers=headers)
soup = BeautifulSoup(req.text, 'xml')

list_catigories_url = soup.find_all('loc')
for item in list_catigories_url:
    item = item.getText()
    list_cat_url.append(item)



# Цикл для перехода по карточкам
for item in tqdm(list_cat_url):
    req = requests.get(item, headers=headers)
    soup = BeautifulSoup(req.text, "lxml")
    # print(soup)
    # exit()

    count += 1
    print(f"Обработка {count} карточки")

    try:
        url = item
    except Exception:
        url = 'none'
    try:
        name = soup.find('h1', class_="text-center").getText()
    except Exception:
        name = 'none'
    try:
        price = re.search('[0-9.]+',soup.find('div', class_="col-3").getText())
    except Exception:
        price = 'none'

    carts.append({
        "url": url,
        "name": name,
        "price": price.group(0),
    })
#     print(carts)
# print(carts)
with open("../resul_parce/dvoroz.json", "w") as file:
        json.dump(carts, file, indent=4, ensure_ascii=False)