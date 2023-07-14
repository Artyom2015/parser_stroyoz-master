import requests
import json
from selenium import webdriver
import time
from bs4 import BeautifulSoup
from tqdm import tqdm

list_cat_url = []
carts = []

start_time = time.time()

SCROLL_PAUSE_TIME = 3

def cart(carts, url, is_file_exist):
    # print("fegrdzggs")
    carts_item = []
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

    car = BeautifulSoup(browser.page_source, "lxml")

    if car.find('div', class_="products-list"):
        cart_div = car.find('div', class_="products-list")
        list_carts = cart_div.find_all('div', class_="product-item")
        for cart_item in list_carts:
            try:
                url_cart = cart_item.find('a').get('href')
            except Exception:
                url_cart = None
            
            try:
                name_cart = cart_item.find('div', class_="desc").find('h3').getText()
            except Exception:
                name_cart = None
            
            try:
                price_cart = cart_item.find('div', class_="main-price-row").find('span', class_="price").getText()
            except Exception:
                price_cart = None

            carts_item.append({
                'url': f"https://xn--80adsfsdepifdc.xn--p1ai{url_cart}",
                'name': name_cart, #.strip()
                'price': price_cart.replace('\n', '').replace(' ', ''),
            })

        with open("../resul_parce/carts_otvinta.json", "a", encoding="utf-8") as file:
            json.dump(carts_item, file, indent=4, ensure_ascii=False)



while True:
    try:
        url = "https://xn--80adsfsdepifdc.xn--p1ai"
        headers = {
            "accept": "*/*",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        }
        #Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium
        browser = webdriver.Chrome()
        browser.get(url)
        #Записать страницу в файл(тест)
        # with open('html_startPage/otvin.html', 'w') as file:
        #     file.write(browser.page_source)
        #Преобразовать в soup объект для поиска
        soup = BeautifulSoup(browser.page_source, "lxml")

        sections = soup.find('nav', class_="category_row")
        link_catigories_list = sections.find_all('li')

        #
        try:
            with open("../exit/pars_stat3.json") as file:
                d = json.load(file)
                file.close()
                is_file_exist1 = True
                is_file_exist2 = True
                is_file_exist3 = True
                is_file_exist4 = True
        except Exception:
            is_file_exist1 = False
            is_file_exist2 = False
            is_file_exist3 = False
            is_file_exist4 = False

        #
        try:
            with open("../exit/pars_stat_detail3.json") as file:
                p = json.load(file)
                file.close()
                is_file_exist = True

        except Exception:
            is_file_exist = False

        list_ex = ["/stock", "/novinki"]
        # try:
        #Получить ссылки на разделы
        for section in link_catigories_list:
            sect = section.find('a').get('href')
            if sect in list_ex:
                continue

            url_section = f"{url}{sect}"  # URL детальной страницы раздела

            if is_file_exist1 == True:
                if sect.strip() != f"{d['1lvl'].strip()}":
                    continue
                else:
                    is_file_exist1 = False


            status_pars = {
                "1lvl": sect,
            }
            with open("../exit/pars_stat3.json", "w") as file:
                json.dump(status_pars, file, indent=4, ensure_ascii=False)


            browser.get(url_section)  # Запрос на получение страницы раздела верхнего уровня
            page = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

            subsections_container = page.find('div', class_="col-sm-12")  # Получить контейнер с подкатегориями
            # print(subsections_container)
            sect_items = subsections_container.find_all('a', class_="sub-catalog-category")  # Получить список подкатегорий

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
                with open("../exit/pars_stat3.json", "w") as file:
                    json.dump(status_pars, file, indent=4, ensure_ascii=False)

                browser.get(url_subsection)  # Запрос на получение страницы раздела верхнего уровня
                page_2 = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

                if page_2.find('div', class_="col-sm-12"):

                    subsections_container2 = page_2.find('div', class_="col-sm-12")  # Получить контейнер с подкатегориями
                    sect_items2 = subsections_container2.find_all('a', class_="sub-catalog-category")  # Получить список подкатегорий

                    for subsection2 in sect_items2:
                        url_subsection_lv2 = subsection2.get('href')
                        url_subsection2 = f"{url}{url_subsection_lv2}"  # URL детальной страницы подраздела

                        if is_file_exist2 == True:
                            if url_subsection_lv2.strip() != f"{d['3lvl'].strip()}":
                                continue
                            else:
                                is_file_exist3 = False

                        status_pars = {
                            "1lvl": sect,
                            "2lvl": url_subsection_lv1,
                            "3lvl": url_subsection_lv2,
                        }
                        with open("../exit/pars_stat3.json", "w") as file:
                            json.dump(status_pars, file, indent=4, ensure_ascii=False)

                        browser.get(url_subsection2)  # Запрос на получение страницы раздела верхнего уровня
                        page_3 = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

                        if page_3.find('div', class_="col-sm-12"):
                            subsections_container3  = page_3.find('div', class_="col-sm-12")  # Получить контейнер с подкатегориями
                            sect_items3 = subsections_container3.find_all('a', class_="sub-catalog-category")  # Получить список подкатегорий
                            for subsection3 in sect_items3:
                                url_subsection_lv3 = subsection3.get('href')
                                url_subsection3 = f"{url}{url_subsection_lv3}"  # URL детальной страницы подраздела

                                if is_file_exist3 == True:
                                    if url_subsection_lv3.strip() != f"{d['4lvl'].strip()}":
                                        continue
                                    else:
                                        is_file_exist3 = False

                                status_pars = {
                                    "1lvl": sect,
                                    "2lvl": url_subsection_lv1,
                                    "3lvl": url_subsection_lv2,
                                    "4lvl": url_subsection_lv3,
                                }
                                with open("../exit/pars_stat3.json", "w") as file:
                                    json.dump(status_pars, file, indent=4, ensure_ascii=False)

                                browser.get(url_subsection3)  # Запрос на получение страницы раздела верхнего уровня
                                page_4 = BeautifulSoup(browser.page_source, "lxml")  # Получить страницу раздела врехнего уровня в формате soup объекта  need lxml

                                is_file_exist = cart(page_4, url_subsection3, is_file_exist)

                        else:
                            is_file_exist = cart(page_3, url_subsection2, is_file_exist)

                else:
                    is_file_exist = cart(page_2, url_subsection, is_file_exist)

        # except Exception as e: print(e)

        print("--- %s seconds ---" % (time.time() - start_time))
        browser.close()
        browser.quit()
        break

    except:
        errors = {
            "error": "Была ошибка",
        }
        with open("../exit/errors3.json", "a", encoding='utf-8') as file:
            json.dump(errors, file, indent=4, ensure_ascii=False)