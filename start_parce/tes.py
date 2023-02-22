import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver



options = webdriver.ChromeOptions()

options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36")

options.add_argument("--disable-blink-features=AutomationControlled")


options.headless = True

driver =

headers = {
    "accept": "*/*",
    ,
}


browser = webdriver.Chrome(ChromeDriverManager().install())
browser.get(f"{url}/catalog")
