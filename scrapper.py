import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

url="https://autoplius.lt/skelbimai/naudoti-automobiliai"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # sometimes headless=True is easier detected
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/114.0.0.0 Safari/537.36",
        locale="en-US",
        java_script_enabled=False,
        bypass_csp=True,
        # Optionally enable storage like cookies, cache
    )
    page = context.new_page()
    page.goto(url)
    # page.wait_for_load_state("networkidle")  # wait for all requests
    html = page.content()
    soup=BeautifulSoup(html, 'html.parser')
    print(soup.prettify())
    browser.close()
