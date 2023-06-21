import requests
import json
import time
from bs4 import BeautifulSoup
import re

start_time = time.time()

def cart(carts, url, is_file_exist):
    if carts.find("a", class_="more_goods lvl2__content-show"):
    # найти последнее значение в пагинации
        container_pagen = carts.find("aside", class_="pager-catalogue lvl2__content-nav").find('div', class_="lvl2__content-nav-numbers")
        last_pagen = int(container_pagen.find('ul', class_="ul-cat-pager").find_all("li")[-1].text.strip())
        # last_pagen = 2
    else:
        last_pagen = 1

    if is_file_exist == True:
        start_pagen = p['pagen']

    else:
        start_pagen = 1

    for i in range(start_pagen, last_pagen):
        if i == last_pagen:
            break

        url_page = f"{url}?PAGEN_2={i}"
        print(url_page)

        req = requests.get(url_page, headers=headers)
        carts_page = BeautifulSoup(req.text, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

        if carts_page.find('article', class_="item-text"):
            continue

        cart_div = carts_page.find('div', class_="item-list-inner")
        list_carts = cart_div.find_all('article', class_="item-list group b-catalog-list-product")
        for cart_item in list_carts:

            carts_url = cart_item.find('div', class_="b-catalog-list-product__section2 caption-list").find('a').get('href')
            detail_url = f"https://www.maxidom.ru{carts_url}"

            try:
                price_cart = cart_item.find('div', class_="b-catalog-list-product__buy wrap-buy").find('span', class_="price-list").find('span', class_="b-catalog-list-product__price").getText()
            except Exception:
                price_cart = None

            if is_file_exist == True:
                print("is_file_exist")
                if carts_url.strip() != f"{p['carts_url'].strip()}":
                    continue
                else:
                    is_file_exist = False

            status_pars_detail = {
                "pagen": i,
                "carts_url": f"{carts_url}",
            }
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail4.json", "w") as file:
                json.dump(status_pars_detail, file, indent=4, ensure_ascii=False)

            req = requests.get(detail_url, headers=headers)
            car_item = BeautifulSoup(req.text, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

            carts_items(car_item, detail_url, price_cart)


def carts_items(car_item, detail_url, price_cart):
    carts_item = []

    url = detail_url

    try:
        name_cart = car_item.find('h1', class_="flypage__product-header title-h1").getText()
    except Exception:
        name_cart = None

    carts_item.append({
        'url': url,
        'name': name_cart.replace('\n', '').strip(), #.strip()
        'price': price_cart.replace('\n', '').replace(' ', ''), #.replace('\n', '').replace(' ', '')
    })

    with open("/Users/artem/Desktop/parser_stroyoz-master/resul_parce/maxidom.json", "a", encoding="utf-8") as file:
        json.dump(carts_item, file, indent=4, ensure_ascii=False)

while True:
    try:
        url = "https://www.maxidom.ru"
        headers ={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.2.987 Yowser/2.5 Safari/537.36",
        }
        url_catalog = f"{url}/catalog/"
        req = requests.get(url_catalog, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')

        sections = soup.find('div', class_="content content_border-radius row-categories group")  # Получить контейнер с секциями
        # print(sections)
        link_catigories_list = sections.find_all('a')

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat4.json") as file:
                d = json.load(file)
                file.close()
                is_file_exist1 = True
                is_file_exist2 = True
                #is_file_exist3 = True
                #is_file_exist4 = True
        except Exception:
            is_file_exist1 = False
            is_file_exist2 = False
            #is_file_exist3 = False
            #is_file_exist4 = False

        #
        try:
            with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat_detail4.json") as file:
                p = json.load(file)
                file.close()
                is_file_exist = True

        except Exception:
            is_file_exist = False

        try:
            #Получить ссылки на разделы
            for section in link_catigories_list:
                sect = section.get('href')
                url_section = f"{url}{sect}"  # URL детальной страницы раздела

                if is_file_exist1 == True:
                    if sect.strip() != f"{d['1lvl'].strip()}":
                        continue
                    else:
                        is_file_exist1 = False


                status_pars = {
                    "1lvl": sect,
                }
                with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat4.json", "w") as file:
                    json.dump(status_pars, file, indent=4, ensure_ascii=False)

                print(url_section)

                req = requests.get(url_section, headers=headers)
                page = BeautifulSoup(req.text, 'lxml')
                # print(page)

                subsections_container = page.find('div', class_="content content_border-radius row-categories group")  # Получить контейнер с подкатегориями
                # print(subsections_container)
                sect_items = subsections_container.find_all('a', class_="it_categories_a_link")  # Получить список подкатегорий

                for subsection in sect_items:
                    url_subsection_lv1 = subsection.get('href')#.find('a', class_="sub-catalog-category")
                    url_subsection = f"{url}{url_subsection_lv1}"  # URL детальной страницы подраздела

                    if is_file_exist2 == True:
                        if url_subsection_lv1.strip() != f"{d['2lvl'].strip()}":
                            continue
                        else:
                            is_file_exist2 = False

                    status_pars = {
                        "1lvl": sect,
                        "2lvl": url_subsection_lv1,
                    }
                    with open("/Users/artem/Desktop/parser_stroyoz-master/exit/pars_stat4.json", "w") as file:
                        json.dump(status_pars, file, indent=4, ensure_ascii=False)

                    print(url_subsection)

                    req = requests.get(url_subsection, headers=headers)  # Запрос на получение страницы раздела верхнего уровня
                    page_2 = BeautifulSoup(req.text, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

                    cart(page_2, url_subsection, is_file_exist)

        except Exception as e: print(e)

        print("--- %s seconds ---" % (time.time() - start_time))
        break

    except:
        errors = {
            "error": "Была ошибка",
        }
        with open("/Users/artem/Desktop/parser_stroyoz-master/exit/errors4.json", "a", encoding='utf-8') as file:
            json.dump(errors, file, indent=4, ensure_ascii=False)

        # python maxidom.py