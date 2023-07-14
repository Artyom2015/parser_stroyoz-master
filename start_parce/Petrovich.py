import requests
import json
import time
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
import ast

url = "https://moscow.petrovich.ru"
api = "https://api.petrovich.ru/catalog/v2.3/sections/"#12101?offset=20&limit=20&sort=popularity_desc&city_code=msk&client_id=pet_site
browser = webdriver.Chrome()

def load_cart(iterator, section):
    time.sleep(4)
    browser.get(f"{api}{section}?offset={iterator}&city_code=msk&client_id=pet_site")
    stst = True

    while stst == True:
        try:
            soup = BeautifulSoup(browser.page_source, 'lxml')
            json_re = soup.find('pre').getText()
            json_re = json.loads(json_re)

            items = json_re['data']['products']
            for item in items:
                name = item['title']
                price = item['price']['retail']

                cart.append ({
                    "url": "API use",
                    "name": name,
                    "price": price,
                })
                
                stst = False
                
        except Exception as e:
            time.sleep(15)
            browser.get(url)
            browser.refresh()
            browser.get(f"{api}{section}?offset={iterator}&city_code=msk&client_id=pet_site")
            print(f"Error in {section}")
            print(e)

browser.get(f"{url}/catalog")
cart = []
soup = BeautifulSoup(browser.page_source, "lxml")

sections = soup.find("section", class_="pt-row").find_all("div", class_="category-list")

for section in sections:
    section_url = section.find('a').get("href")
    
    browser.get(f"{url}{section_url}")
    soup = BeautifulSoup(browser.page_source, "lxml")

    sub_sections = soup.find("div", class_="catalog-subsections-list-zero").find_all("div", class_="catalog-subsections-list-item")

    iter = 0

    for sub_section in sub_sections:
        sub_section_url = sub_section.find("a", class_="catalog-subsection").get("href").split("/")
        api_section = sub_section_url[-2]

        browser.get(f"{api}{api_section}?offset=0&city_code=msk&client_id=pet_site")
        keke = True

        while keke == True:
            try:
                soup = BeautifulSoup(browser.page_source, 'lxml')
                json_re = soup.find('pre').getText()
                json_re = json.loads(json_re)
                keke = False
            except Exception:
                time.sleep(15)
                browser.get(url)
                browser.refresh()
                browser.get(f"{api}{api_section}?offset=0&city_code=msk&client_id=pet_site")
                print(f"Error in section {api_section}")

        resp_count = json_re['data']['pagination']['products_count']

        for i in range(0, resp_count, 20):
            load_cart(i, api_section)

        print(f"Done subsection code {api_section}")
    print(f"Done!!!! {section_url}")
        
with open("../resul_parce/Petrovich1.json", "w", encoding="utf-8") as file:
    json.dump(cart, file, indent=4, ensure_ascii=False)