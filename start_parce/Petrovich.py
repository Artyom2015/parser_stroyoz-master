import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url = "http://dvoroz.ru/dvoroz/inetshop/shop"

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "uUser-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

req = requests.get(url, headers=headers)

soup = BeautifulSoup(req.text, "lxml")

list_catigories_1lv = soup.find_all('a', class_="aname")
for item in tqdm(list_catigories_1lv):
    req = requests.get(f"http://dvoroz.ru{item.get('href')}", headers=headers)
    soup = BeautifulSoup(req.text, "lxml")

    list_catigories_2lv = soup.find_all('a', class_="aname")
        for item_page in list_catigories_2lv:
            req = requests.get(f"http://dvoroz.ru{item_page.get('href')}", headers=headers)
            soup = BeautifulSoup(req.text, "lxml")
#
# for item in tqdm(list_cat_url):
#     req = requests.get(item['url_cat'])
#     soup = BeautifulSoup(req.text, "lxml")
