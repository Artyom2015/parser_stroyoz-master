import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

start_time = time.time()
url = "https://www.maxidom.ru"
headers = {
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
}
url_catalog = f"{url}/catalog"
req = requests.get(url_catalog, headers=headers)
src = req.text
soup = BeautifulSoup(src, "lxml")

all_catigories_1lvl = soup.find('div', class_="row-categories group").find_all('a', class_="it_categories_a")
all_catigories_1lvl_list = []

for item in all_catigories_1lvl:
    tes = item.get('href')
    all_catigories_1lvl_list.append(f"{url}{tes}")

    all_catigories_1lvl = soup.find('div', class_="row-categories group").find_all('a', class_="it_categories_a")
for item in tqdm(all_catigories_1lvl_list):
    req = requests.get(f"{url_catalog}{item}", headers=headers).text
    soup = BeautifulSoup(req, "lxml")

# Нужно взять ссылку из второго тега <a> но у него нет класса

