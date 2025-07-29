import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url="https://autoplius.lt/skelbimai/naudoti-automobiliai"

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    soup=BeautifulSoup(str(page))
    print(soup)
    browser.close()