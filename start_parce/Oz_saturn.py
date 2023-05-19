import requests
import json
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
import js2py

list_cat_url = []

PAUSE_TIME = 2

carts = []
count = 0

start_time = time.time()

#получить карточки
def carts(car, url, is_file_exist):
    count = 0
    if car.find("ul", class_="pagination"):
    # найти последнее значение в пагинации
        last_pagen = int(car.find("ul", class_="pagination").find_all("li")[-2].text.strip())
        # last_pagen = 2
    else:
        last_pagen = 1

    for i in range(1, last_pagen):
        if i == last_pagen:
            break
        print(f"Кнопка нажата: {i}")
        browser.execute_script("document.querySelector('button.btn.btn-outline-revers-primary').click();")
        time.sleep(1)
    ca_item = BeautifulSoup(browser.page_source, "lxml")

    item_carts = ca_item.find('div', class_='block-goods').find_all('div', class_='goods-name')
    # try:
    for item_car in item_carts:

        detail_url = item_car.find('a', class_="g").get('href')

        if is_file_exist == True:
            print("is_file_exist")
            if detail_url.strip() != f"{p['detail_url'].strip()}":
                continue
            else:
                is_file_exist = False

        status_pars_detail = {
            # "pagen": i,
            "detail_url": f"{detail_url}",
        }
        with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail1.json", "w") as file:
            json.dump(status_pars_detail, file, indent=4, ensure_ascii=False)

        browser.get(url=f"https://oz.saturn.net{detail_url}")

        count += 1

        url_sections = browser.current_url
        print(F"{url_sections} : карточки {count}")

        car_item = BeautifulSoup(browser.page_source, "lxml")

        carts_items(car_item)
    # except Exception as e: print(e)

#получить данные из карточек
def carts_items(car_item):
    carts = []
    url = browser.current_url
    # print(F"{url} : карточки")
    try:
        name = car_item.find('h1', class_="_goods-title").getText()
        # print(name.replace('\n', ' ').replace('\t', ' ').strip())
    except Exception:
        name = 'none'
        # print(name)
    try:
        if car_item.find('div', class_="price-base"):
            price = car_item.find('div', class_="price-base").getText()
            # print(price.replace('Ä', ' ').replace('\n', ' ').replace('\t', ' ').strip())
        else:
            price = car_item.find('div', class_="price-wrapper").find('span', class_="price block-price-value").getText()
            # print(price.replace('Ä', ' ').replace('\n', ' ').replace('\t', ' ').strip())
    except Exception:
        price = 'none'
        # print(price)

    carts.append({
        "url": url,
        "name": name.replace('\n', ' ').replace('\t', ' ').replace(' ', ' ').strip(),
        "price": price.replace('Ä', ' ').replace('\n', ' ').replace('\t', ' ').replace(' ', '').replace('штм', 'шт').strip(),
    })

    with open("/Users/artem/Desktop/parser_stroyoz-master/resul_parce/Oz_Saturn.json", "a", encoding="utf-8") as file:
        json.dump(carts, file, indent=4, ensure_ascii=False)


while True:
    try:
        browser = webdriver.Chrome()  # ChromeDriverManager().install()

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }
        url = "https://oz.saturn.net"
        # Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium

        browser.get(f"{url}/catalog")

        # Преобразовать в soup объект для поиска
        sections = BeautifulSoup(browser.page_source, "lxml")

        # переход по разделам
        # Работа на формирование главных разделов
        home_catigories_sections = sections.find('nav', class_="_category_level2-nav")  # Получить контейнер в котором храняться раделы первого уровня
        list_categories_sections = home_catigories_sections.find_all('li', class_='_category_nav-item')  # Список контейнеров

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat1.json") as file:
                d = json.load(file)
                file.close()
                is_file_exist1 = True
        except Exception:
            is_file_exist1 = False

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail1.json") as file:
                p = json.load(file)
                file.close()
                is_file_exist = True

        except Exception:
            is_file_exist = False

        # Пройтись по разделам каталога верхнего уровня
        for section in list_categories_sections:
            name_section = section.find('span', class_='_category_nav-title').text.strip()  # Название раздела
            url_pictures_section = section.find('span', class_='b_baner').find('img').get('src')  # URL картинки раздела
            url_p_section = section.find('a').get('href')
            url_section = f"{url}{url_p_section}"  # URL детальной страницы раздела

            if is_file_exist1 == True:
                if url_p_section.strip() != f"{d['1lvl'].strip()}":
                    continue
                else:
                    is_file_exist1 = False


            status_pars = {
                "1lvl": url_p_section,
            }
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat1.json", "w") as file:
                json.dump(status_pars, file, indent=4, ensure_ascii=False)


            # Зайти внутрь разделов верхнего уровня
            browser.get(url_section)  # Запрос на получение страницы раздела верхнего уровня
            soup_subsection = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

            is_file_exist = carts(soup_subsection, url_section, is_file_exist)

        print("--- %s seconds ---" % (time.time() - start_time))
    except:
        errors = {
            "error": "Была ошибка",
        }
        with open("/Users/artem/Desktop/parser_stroyoz-master/exit/errors1.json", "a", encoding='utf-8') as file:
            json.dump(errors, file, indent=4, ensure_ascii=False)

