import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url="https://autoplius.lt/skelbimai/naudoti-automobiliai"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/114.0.0.0 Safari/537.36",
        locale="en-US",
        java_script_enabled=False,
        bypass_csp=True,
    )
    page = context.new_page()
    page.goto(url)
    html = page.content()

    soup=BeautifulSoup(html, 'html.parser')
    shop_div=soup.find("div", {"class" : "auto-lists lt"})

    car_list_part=shop_div.find_all("a", {"class" : "announcement-item is-enhanced is-gallery"})
    car_links=[link.get("href") for link in car_list_part]
    print(car_links)
    next_page=url+soup.find("a", {"class" : "next"}).get("href")
    print(next_page)
    # tag='<div class="auto-lists lt">'
    # tag=BeautifulSoup(tag).b
    #
    # car_links=BeautifulSoup.find_all(tag, recursive=True)
    # print(car_links)
    browser.close()
