import time
import csv
from enum import Enum
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


class PropzyEntity(Enum):
    PROJECT_NAME='name-project'
    INVESTOR = 'name-investor'
    META = 'meta-data'
    URL = 'url'
    ICON_PATH = 'icon-path'

class PropzyCrawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")

    def open(self):
        pass

    def action(self):
        url = "https://propzy.vn/mua/bat-dong-san/hcm?sortBy=price&sortDirection=ASC&tags=hcm&type=mua"
        self.driver.get(url)
        propzy_df = list()
        for num_pages in range(1):
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            info_items = self.driver.find_element(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]")
            info_items = info_items.find_elements(By.XPATH, "./*")
            print("Number of items: ", len(info_items))
            for item in info_items:
                item_dict = dict()
                item_dict['link'] = item.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').get_attribute("href")
                item_dict['brief'] = item.find_element(By.TAG_NAME, 'h3').find_element(By.TAG_NAME, 'a').text
                item_dict['id'] = item_dict['link'].split('/')[-1]
                item_dict['price'] = item.find_element(By.CLASS_NAME, "format-price").text
                item_dict['price_per_unit'] = item.find_element(By.CLASS_NAME, "format-unit-price").text
                item_dict['address'] = item.find_element(By.CLASS_NAME, "address").text
                facilities = item.find_element(By.CLASS_NAME, "facilities");
                facilities = facilities.find_elements(By.XPATH, "./*")
                item_dict['facilities_key'] = list()
                item_dict['facilities_value'] = list()
                for fac in facilities:
                    item_dict['facilities_key'].append(fac.find_element(By.TAG_NAME,"i").get_attribute("class"))
                    item_dict['facilities_value'].append(fac.find_element(By.TAG_NAME,"span").text)
                propzy_df.append(item_dict)
            pd_data = pd.DataFrame(propzy_df)
            pd_data.to_csv(f"./page_{num_pages}.csv")
            time.sleep(1)

            while True:
                pageHeight = self.driver.execute_script("return document.body.scrollHeight")
                totalScrolledHeight = self.driver.execute_script("return window.pageYOffset + window.innerHeight")
                if (pageHeight-1) <= totalScrolledHeight:
                    break
                else:
                    continue
                    time.sleep(1)

            time.sleep(1)
            btns = self.driver.find_elements(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/ul/li[8]/div")
            if len(btns) == 0:
                btns = self.driver.find_elements(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/ul/li[9]/div")
            if len(btns) == 0:
                print("Cant get components")
                time.sleep(100)
                break
            btns[0].click()
        self.driver.close()

    def close(self):
        pass

