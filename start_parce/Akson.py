import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from tqdm import tqdm
import time
import json
import traceback
import response

list_cat_url = []
count = 0
carts = []
PAUSE_TIME = 2

start_time = time.time()
url = "https://akson.ru/c/moskva/"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

def repeat(item):
        browser.get(item['url_cat'])

        time.sleep(4)

        page = BeautifulSoup(browser.page_source, "lxml")

        if page.find('div', class_="sections"):
            # print("Есть подразделы")
            section_con = page.find('div', class_="sections")
            section_list = section_con.find_all('a', class_="section")
            section_list_done = []
            for section_item in section_list:
                section_list_done.append({
                    "url_cat": f"https://akson.ru{section_item.get('href')}"
                })

            # print(section_list_done)
            section(section_list_done)
            # print(section_list_done)
        else:
            # print("cart")
            cart_con = BeautifulSoup(browser.page_source, "lxml")
            # pages = cart_con.find('div', class_="pagination")
            if cart_con.find('div', class_="catalog__right"):
                # cart_con = cart_con.find('div', class_="goods-list__content")
                # cart(cart_con)
                if cart_con.find("div", class_="pagination"):
                    pages_count = int(
                        cart_con.find("div", class_="pagination").find_all("span", class_="pagination__item")[-1].text)
                    # print(pages_count)
                    # цикл по пагинации
                    for i in range(1, pages_count + 1):
                        if i == 1:
                            url_page = item['url_cat']
                        else:
                            url_page = f"{item['url_cat']}?page={i}"
                        # print(url_page)
                        time.sleep(4)
                        browser.get(url_page)
                        # cart_con = BeautifulSoup(browser.page_source, "lxml")
                        # cart(cart_con)
                        # cart_con = cart_con.find('div', class_="goods-list__content")
                        cart(cart_con)
                    cart_con = cart_con.find('div', class_="goods-list__content")
                    cart(cart_con)

def cart(cart_con):
    try:

        list_cart = cart_con.find_all('div', class_="product-matrix")
        for cart in list_cart:
            url = "https://akson.ru" + cart.find('a', class_="info-title").get('href')
            name = cart.find('a', class_="info-title").find('span').getText()
            price = cart.find('div', class_="info-price__block").find('span', class_="info-price__value").getText()
            # print(name)
            # print()
            carts.append({
                "url": f"{url}",
                "name": name,
                "price": price,
            })

    except Exception:
        print(carts)
                # print(carts)
def section(list_cat_url):
    # print(list_cat_url)
    for item in list_cat_url:
        # print(item)
        browser.get(item['url_cat'])

        time.sleep(4)
        page = BeautifulSoup(browser.page_source, "lxml")

        if page.find('div', class_="sections"):
            # print("Есть подразделы")
            section_con = page.find('div', class_="sections")
            section_list = section_con.find_all('a', class_="section")
            section_list_done = []
            for section_item in section_list:
                section_list_done.append({
                    "url_cat": f"https://akson.ru{section_item.get('href')}"
                })

            # print(section_list_done)
            section(section_list_done)
            # print(section_list_done)
        else:
            # print("cart")
            cart_con = BeautifulSoup(browser.page_source, "lxml")
            # pages = cart_con.find('div', class_="pagination")
            if cart_con.find('div', class_="catalog__right"):
                # cart_con = cart_con.find('div', class_="goods-list__content")
                # cart(cart_con)
                if cart_con.find("div", class_="pagination"):
                    pages_count = int(
                        cart_con.find("div", class_="pagination").find_all("span", class_="pagination__item")[-1].text)
                    # print(pages_count)
                    # цикл по пагинации
                    for i in range(1, pages_count + 1):
                        if i == 1:
                            url_page = item['url_cat']
                        else:
                            url_page = f"{item['url_cat']}?page={i}"
                            # print(url_page)
                        time.sleep(4)
                        browser.get(url_page)
                        # cart_con = BeautifulSoup(browser.page_source, "lxml")
                        # cart(cart_con)
                        # cart_con = cart_con.find('div', class_="goods-list__content")
                        cart(cart_con)
                    cart_con = cart_con.find('div', class_="goods-list__content")
                    cart(cart_con)

            else:
                repeat(item)
                print("else работает")

        #section("section")
        # soup = BeautifulSoup(browser.page_source, "lxml")
        # if soup.find('div', class_="sections").find_all('a', class_="section"):
        #     browser.get(item['url_cat'])

# Сайт на VUE поэтому request не работает, эмулируем работу браузера через selenium
browser = webdriver.Chrome()
browser.get(url)

soup = BeautifulSoup(browser.page_source, "lxml")
# print(soup)
link_catigories_list = soup.find('div', class_="sections").find_all('a', class_="section")
# print(link_catigories_list)
list = ["/sozday_sam/", "/ready_made_solutions/", "/c/moskva/vodosnabzhenie_otoplenie/", "/c/moskva/ventilyatsiya/", "/c/moskva/elektrotovary/", "/c/moskva/skobyanye_izdeliya_i_krepezh/", "/c/moskva/keramicheskaya_plitka/", "/c/moskva/kraski/", "/c/moskva/instrumenty/", "/c/moskva/santehnika/", "/c/moskva/oboi/", "/c/moskva/otdelka_sten_i_potolkov/", "/c/moskva/napolnye_pokrytiya/", "/c/moskva/dveri_i_okna_lestnitsy/", "/c/moskva/okna/", "/c/moskva/lestnitsy/", "/c/moskva/sistemy_hraneniya/", "/c/moskva/osveschenie/", "/c/moskva/mebel/", "/c/moskva/interer_i_dekor/", "/c/moskva/bytovaya_tehnika/", "/c/moskva/avtotovary/", "/c/moskva/otdyh_i_hobbi/", "/c/moskva/tovary_dlya_doma/", "/c/moskva/posuda/", "/c/moskva/tovary_dlya_sada/", "/c/moskva/umnyy_dom/"]

for item in link_catigories_list:

    item = item.get('href')
    if item in list:
        continue
    list_cat_url.append({
        "url_cat": f"https://akson.ru{item}",
    })

section(list_cat_url)
# if soup.find('div', class_="sections"):

    # else:
    #     continue
        # print(list_cat_url)
# for item in tqdm(list_cat_url):
#     req = requests.get(item['url_cat'], headers=headers)
#     soup = BeautifulSoup(req.text, "lxml")

with open("../resul_parce/Akson.json", "w", encoding="utf-8") as file:
    json.dump(carts, file, indent=4, ensure_ascii=False)

end = time.time() - start_time ## собственно время работы программы
print(end)
browser.close()
browser.quit()