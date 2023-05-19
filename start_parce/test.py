import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import js2py
import re
import pandas as pd


start_time = time.time()

# def section(page):
#     # count = 0
#     if page.find('ul', class_="new-folders-menu2"):
#         sect_items = page.find('ul', class_="new-folders-menu2").find_all('li')
#
#         for item in sect_items:
#             # if count > 1:
#             #     continue
#
#             browser.get(f"https://1001krep.ru{item.find('a').get('href')}")
#             pag = BeautifulSoup(browser.page_source,"lxml")
#             # count += 1
#             section(pag)
#     else:
#         carts = BeautifulSoup(browser.page_source, "lxml")
#         cart(carts)


def cart(carts, url, is_file_exist):
    # count = 0
    if carts.find('ul', class_="shop2-pagelist"):
        pagens_items = carts.find('li', class_="page-last").find('a')
        last_pagens = pagens_items.get('href')
        pagen_item = last_pagens.split("/")
        last_pagen = int(pagen_item[-1])
        # url_page = browser.current_url
    else:
        last_pagen = 1

    if is_file_exist == True:
        start_pagen = p['pagen']
    else:
        start_pagen = 0
    for i in range(start_pagen, last_pagen + 1):
        # if i == last_pagen+1:
        #     break
        browser.get(url=f"{url}/p/{i}")
        print(f"{url}/p/{i}")
        carts = BeautifulSoup(browser.page_source, "lxml")
        count = 0
        if carts.find('div', class_="product-list"):
            carts_items = carts.find('div', class_="product-list").find_all('div', class_="shop2-product-item-in")
            for item_cart in carts_items:
                # if count > 1:
                #     continue

                detail_url = item_cart.find('a').get('href')

                if is_file_exist == True:
                    print("is_file_exist")
                    if detail_url.strip() != f"{p['detail_url'].strip()}":
                        continue
                    else:
                        is_file_exist = False

                status_pars_detail = {
                    "pagen": i,
                    "detail_url": f"{detail_url}",
                }
                with open("/Users/artem/Desktop/parser_protorg/resul_parse/pars_stat_detail1.json", "w") as file:
                    json.dump(status_pars_detail, file, indent=4, ensure_ascii=False)

                # if is_file_ready == True:
                #     print("is_file_ready")
                #     if detail_url.strip() != f"{r['detail_url'].strip()}":
                #         continue
                #     else:
                #         is_file_ready = False
                #
                # status_pars_ready = {
                #     "detail_url": f"{detail_url}",
                # }
                # with open("/Users/artem/Desktop/parser_protorg/resul_parse/1001krep.json.json", "w") as file:
                #     json.dump(status_pars_ready, file, indent=4, ensure_ascii=False)

                browser.get(f"https://1001krep.ru{detail_url}")
                url_page = browser.current_url
                print(url_page)
                car = BeautifulSoup(browser.page_source,"lxml")
                count += 1
                print(f"Обработана карточка: {count}")
                cart_item(car)

def cart_item(car):
    count = 0
    carts = []
    table_mod = car.find('div', class_="product-data").find_all('div', class_="td column-name")
    # try:
    for item_mod in table_mod:
        # if count > 3:
        #     continue
        carts_url = item_mod.find('a').get('href')
        browser.get(f"https://1001krep.ru{carts_url}")
        modif = BeautifulSoup(browser.page_source, "lxml")
        url = browser.current_url
        name = modif.find('h1').getText()
        # print(name)
        description = []
        item_des = modif.find('div', class_="info").find_all('li')
        for desc_item in item_des:
            try:
                if desc_item.find('p'):
                    descript = desc_item.find('p').getText()
                    if "Описание и особенности:" in descript:
                        description = descript
                        # print(description)
                    else:
                        continue
                else:
                    continue
            except Exception:
                description = 'error'
                print(description)
        if not description:
            description = 'none'
            # print(description)

        table = modif.find('div', class_="kinds_table")
        try:
            articl = table.find('div', class_="td art").getText()
            # print(articl)
        except Exception:
            articl = 'none'
            # print(articl)
        try:
            packaging = table.find('div', class_="td param itm_upakovka").getText()
            # print(packaging)
        except Exception:
            packaging = 'none'
            # print(packaging)
        try:
            if table.find('div', class_="price_zero"):
                price = 'Уточнить у менеджера'
                # print(price)
            else:
                price = table.find('div', class_="td price").getText()
                # print(price)
        except Exception:
            price = 'none'
            # print(price)
        try:
            par_item = modif.find('div', class_="product-data").find('div', class_='table-wrapper').find('tbody')
            # parameters = par_item
            parameters = ""
            for item_par in par_item.find_all('tr'):
                table_header = item_par.find('th').text
                table_body = item_par.find('td').text
                parameters += f"{table_header} : {table_body} " ""
                #table_item.append(parameters)
            # print(table_item)
        except Exception:
            parameters = ' '
        count += 1
        print(f"Модификация: {count}")

        carts.append({
            "url": url,
            "name": name.replace('\n', ' ').replace('\t', ' ').strip(),
            "description": description.replace(' ', ' ').replace('\n', ' ').replace('\t', ' ').strip() + " " + parameters,
            # "parameters": parameters.replace('\n', ' ').replace('\t', ' '),
            "articl": articl.replace(':', ' : '),
            "packaging": packaging.replace(':', ' : '),
            "price": price,
        })
    with open("/Users/artem/Desktop/parser_protorg/resul_parse/1001krep.json", "a", encoding="utf-8") as file:
        json.dump(carts, file, indent=4, ensure_ascii=False)
    # except Exception as e: print(e)


while True:
    try:
        browser = webdriver.Chrome()

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        url = "https://1001krep.ru/kategorii-magazina"

        browser.get(url)

        catalogs = BeautifulSoup(browser.page_source, "lxml")

        # переход по разделам
        # Работа на формирование главных разделов
        home_catigories_sections = catalogs.find('ul', class_="categories")  # Получить контейнер в котором храняться раделы первого уровня
        list_categories_sections = home_catigories_sections.find_all('li', class_="level_1")  # Список контейнеров

        #
        try:
            with open("/Users/artem/Desktop/parser_protorg/resul_parse/pars_stat1.json") as file:
                d = json.load(file)
                file.close()
                is_file_exist1 = True
                is_file_exist2 = True
        except Exception:
            is_file_exist1 = False
            is_file_exist2 = False

        #
        try:
            with open("/Users/artem/Desktop/parser_protorg/resul_parse/pars_stat_detail1.json") as file:
                p = json.load(file)
                file.close()
                is_file_exist = True

        except Exception:
            is_file_exist = False

        # try:
        #     with open("/Users/artem/Desktop/parser_protorg/resul_parse/1001krep.json") as file:
        #         r = json.load(file)
        #         file.close()
        #         is_file_ready = True
        #
        # except Exception:
        #     is_file_ready = False

        # try:
        # print(list_catigories_1lv)
        for item in list_categories_sections:
            # print(item)
            url_section_lv1 = item.find('a').get('href')
            url_section = f"https://1001krep.ru{url_section_lv1}"  # URL детальной страницы раздела
            # time.sleep(2)

            if is_file_exist1 == True:
                if url_section_lv1.strip() != f"{d['1lvl'].strip()}":
                    continue
                else:
                    is_file_exist1 = False

            status_pars = {
                "1lvl": url_section_lv1,
            }
            with open("/Users/artem/Desktop/parser_protorg/resul_parse/pars_stat1.json", "w") as file:
                json.dump(status_pars, file, indent=4, ensure_ascii=False)

                # Зайти внутрь разделов верхнего уровня
            browser.get(url_section)  # Запрос на получение страницы раздела верхнего уровня
            page = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

            # is_file_exist = section(page,url_section, is_file_exist)
            subsections_container = page.find('ul', class_='new-folders-menu2')  # Получить контейнер с подкатегориями
            sect_items = subsections_container.find_all('li')  # Получить список подкатегорий
            # print(sect_items)
            for subsection in sect_items:
                #name_subsection = subsection.find('div', class_='category-caption').text.strip()  # Название подраздела
                #url_pictures_subsection = subsection.find('picture', class_='category-image').find('img').get('src')  # URL картинки подраздела
                url_subsection_lv1 = subsection.find('a').get('href')
                url_subsection = f"https://1001krep.ru{url_subsection_lv1}"  # URL детальной страницы подраздела

                if is_file_exist2 == True:
                    if url_subsection_lv1.strip() != f"{d['2lvl'].strip()}":
                        continue
                    else:
                        is_file_exist2 = False

                status_pars = {
                    "1lvl": url_section_lv1,
                    "2lvl": url_subsection_lv1,
                }
                with open("/Users/artem/Desktop/parser_protorg/resul_parse/pars_stat1.json", "w") as file:
                    json.dump(status_pars, file, indent=4, ensure_ascii=False)

                browser.get(url_subsection)  # Запрос на получение страницы раздела верхнего уровня
                page_2 = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

                is_file_exist = cart(page_2, url_subsection, is_file_exist)

        print("--- %s seconds ---" % (time.time() - start_time))
        browser.close()
        browser.quit()
    except:
        errors = {
            "error": "Была ошибка",
        }
        with open("/Users/artem/Desktop/parser_protorg/resul_parse/errors1.json", "a", encoding='utf-8') as file:
            json.dump(errors, file, indent=4, ensure_ascii=False)