import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By



class VhomeCrawler:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920x1080")

        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="./chromedriver")

    def open(self):
        url = "https://vhome.vnexpress.net/du-an?limit=6"
        self.driver.get(url)

    def action(self):
        max_get = -1
        max_v = None
        for _ in range(100):
            btn_show_more = self.driver.find_element(By.XPATH, '//*[@id="viewmore-project"]')
            if max_get >= len(self.driver.find_elements(By.CLASS_NAME, "project  ")): #Cant get any more
                break
            max_v = self.driver.find_elements(By.CLASS_NAME, "project  ")
            max_get = len(self.driver.find_elements(By.CLASS_NAME, "project  "))
            btn_show_more.click()
            time.sleep(.7)
        data = [x.text for x in max_v]
        with open("./data/vhome.txt", 'w') as f:
            for x in data:
                f.write(x)
                f.write('\n\n')

    def close(self):
        self.driver.close()

