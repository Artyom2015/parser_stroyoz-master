import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import re

# def my_strip(price):
#     listw = list(price)
#     try:
#         for i, value in enumerate(listw):
#             if(value == "&"):
#                 start = i
#             if (value == ";"):
#                 end = i
#
#         for i in range(start, end+1):
#             listw[i] = ""
#
#         p = ''.join(listw)
#         return p
#     except:
#         return price


start_time = time.time()

list_cat_url = []
count = 0
carts = []

SCROLL_PAUSE_TIME = 10


while True:
    try:
        url = "https://www.sdvor.com/moscow"
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
        }

        # Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium
        browser = webdriver.Chrome()
        browser.get(url)

        browser.execute_script("document.querySelector('.cx-icon.catalog.icon-m').click();")
        time.sleep(15)

        # Преобразовать в soup объект для поиска
        section = BeautifulSoup(browser.page_source, "lxml")

        list_section = section.find('div', class_="menu-columns")
        link_catigories_list = list_section.find_all('li', class_="has-children")

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat2.json") as file:
                d = json.load(file)
                file.close()
                is_file_exist1 = True
        except Exception:
            is_file_exist1 = False

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail5.json") as file:
                p = json.load(file)
                file.close()
                is_file_exist = True

        except Exception:
            is_file_exist = False

        # try:
        # Получить ссылки на разделы
        for item in link_catigories_list:
            section_pages = item.find('a', class_="link").get('href')
            text_section = item.find('a', class_="link").getText()
            print(f"{text_section}: {section_pages}")
            if section_pages == "https://www.sdvor.com/moscow/category/prokat-instrumenta-98001":
                continue

            if is_file_exist1 == True:
                if section_pages.strip() != f"{d['1lvl'].strip()}":
                    continue
                else:
                    is_file_exist1 = False

            status_pars = {
                "1lvl": section_pages,
            }
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat2.json", "w") as file:
                json.dump(status_pars, file, indent=4, ensure_ascii=False)

            browser.get(section_pages)
            carts_pages = BeautifulSoup(browser.page_source, "lxml")

            # Get scroll height
            last_height = browser.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = browser.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            full_pages = BeautifulSoup(browser.page_source, "lxml")

            products_list = full_pages.find('div', class_='product-grid-items')
            link_products_list = products_list.find_all('div', class_='product')

            for item_cart in link_products_list:
                count += 1
                
                carts_url = item_cart.find('a', class_="product-name").get('href')

                if is_file_exist == True:
                    print("is_file_exist")
                    if carts_url.strip() != f"{p['carts_url'].strip()}":
                        continue
                    else:
                        is_file_exist = False

                status_pars_detail = {
                    # "pagen": i,
                    "carts_url": carts_url,
                }
                with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail5.json", "w") as file:
                    json.dump(status_pars_detail, file, indent=4, ensure_ascii=False)

                try:
                    url = item_cart.find('a', class_="product-name").get('href')
                except Exception:
                    url = 'none'
                try:
                    name = item_cart.find('a', class_="product-name").getText()
                except Exception:
                    name = 'none'
                try:
                    # price = re.search('[0-9.]+', item_cart.find('span', class_="main").getText())
                    price = item_cart.find('div', class_="price").getText()
                except Exception:
                    price = 'none'

                carts.append({
                    "url": f"{url}",
                    "name": name.strip(),
                    # "price": price.group(0).strip(),
                    "price": price.replace(' ', ' ').strip(),
                })
                
            print(count)

        # except Exception as e: print(e)

        with open("/Users/artem/Desktop/parser_stroyoz-master/resul_parce/sdvor.json", "w", encoding="utf-8") as file:
            json.dump(carts, file, indent=4, ensure_ascii=False)

        end = time.time() - start_time ## собственно время работы программы
        print(end)
        break
    except:
        errors = {
            "error": "Была ошибка",
        }
        with open("/Users/artem/Desktop/parser_stroyoz-master/exit/errors2.json", "a", encoding='utf-8') as file:
            json.dump(errors, file, indent=4, ensure_ascii=False)