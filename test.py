import time

import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

url = "https://www.happycow.net/oceania/australia/new_south_wales/sydney/"

# all methods below yield the same output - cannot access nodes any deeper than ".city-results"

# using selenium webdriver
def selenium_webdriver():
    service = Service(executable_path=ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service)
    browser.get(url)
    restuarants = browser.find_element(By.CLASS_NAME, "city-results")
    print(restuarants.text)
    browser.quit()

# using requests & beautifulsoup4
def beautifulsoup4():
    html = requests.get(url).text
    time.sleep(10)
    soup = BeautifulSoup(html, "html.parser")
    restuarants = soup.find(class_="venue-city-items")  # this fails - returns NoneType
    print(restuarants.prettify())

# using requests-html (supposedly has support for JavaScript)
def requests_html():
    session = HTMLSession()
    r = session.get(url)
    r.html.render(sleep=1, keep_page=True, scrolldown=1)
    restuarants = r.html.find(".venue-list-item")
    print(restuarants)

# beautifulsoup4()
# selenium_webdriver()
requests_html()
