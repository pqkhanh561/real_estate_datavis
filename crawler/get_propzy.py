import time
from enum import Enum

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
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        btns = self.driver.find_elements(By.XPATH, "//*[@id=\"__next\"]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/ul/li[8]/div")
        btns[0].click()
        time.sleep(5)
        self.driver.close()

    def close(self):
        pass

