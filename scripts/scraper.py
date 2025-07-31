import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from typing import Tuple, Dict, List
import pandas as pd

url="https://autoplius.lt/skelbimai/naudoti-automobiliai/volkswagen/golf?category_id=2&slist=2628362265"
user=("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/114.0.0.0 Safari/537.36")
file = "results.csv"
car_dict={"Kaina":[],
          "Pirma registracija": [],
          "Rida": [],
          "Variklis": [],
          "Kuro tipas" : [],
          "Kėbulo tipas": [],
          "Durų skaičius": [],
          "Varantieji ratai":[],
          "Klimato valdymas": [],
          "Spalva": [],
          "Ratlankių skersmuo": [],
          "Nuosava masė, kg": [],
          "Sėdimų vietų skaičius": [],
          "Pirmosios registracijos šalis": [],
          "Link": []}

def get_cars(html:str)->Tuple[List[str],str]:

    soup=BeautifulSoup(html, 'html.parser')

    shop_div=soup.find("div", {"class" : "auto-lists lt"})
    car_list_part=shop_div.find_all("a", {"class" : "announcement-item is-enhanced is-gallery"})
    car_links=[link.get("href") for link in car_list_part]

    next_page=url+soup.find("a", {"class" : "next"}).get("href")

    return car_links,next_page
def get_info(car_html:str):
    return None


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=user,
            locale="en-US",
            java_script_enabled=True,
            bypass_csp=True,
        )
        page = context.new_page()
        page.goto(url)
        html = page.content()

        page_count=1
        car_count=0

        #while page is not None:
        page_count+=1
        car_lists,next_page=get_cars(html)
        for car in car_lists:
            page.goto(car)

            html=page.content()
            soup = BeautifulSoup(html, 'html.parser')

            parameter_block=soup.find("div", {"class": "row announcement-section"})

            parameter_names=parameter_block.find_all("div", {"class": "parameter-label"})
            parameter_values=parameter_block.find_all("div", {"class": "parameter-value"})

            par=[parameter.string.strip() for parameter in parameter_names if parameter.string.strip()!='Kėbulo numeris (VIN)']
            par_values=[parameter.string.replace('\n','').strip()
                        for parameter in parameter_values if parameter.string is not None]

            car_object=dict(zip(par,par_values))
            car_object["Link"]=car

            for key in car_dict.keys():
                notSeen=True
                for keyT in car_object.keys():
                    if key==keyT:
                        notSeen=False
                        car_dict[key].append(car_object[key])
                if notSeen:
                    car_dict[key].append(None)

        car_count += len(car_lists)
        #page.goto(next_page)

        print(f"\nGoing to next page: {page_count}\n")
        print(f"\nCurrent scrapped car count:{car_count}\n")

        #html=page.content()
        browser.close()

    dt=pd.DataFrame(data=car_dict)
    dt.to_csv(file, mode='w')