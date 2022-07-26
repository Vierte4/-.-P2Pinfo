import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.config import bybit_user_path
from data.urls import *


class BybitChecker():
    def __init__(self, driver: webdriver.Chrome):
        self.data = \
            {'usdt_buy_rosbank': [8, bybit_usdt_buy_rosbank, 'L3', 0],
             'usdt_sell_rosbank': [9, bybit_usdt_sell_rosbank, 'L4', 0],
             'usdt_buy_tinkoff': [10, bybit_usdt_buy_tinkoff, 'L5', 0],
             'usdt_sell_tinkoff': [11, bybit_usdt_sell_tinkoff, 'L6', 0],
             'btc_buy_rosbank': [12, bybit_btc_buy_rosbank, 'M3', 0],
             'btc_sell_rosbank': [13, bybit_btc_sell_rosbank, 'M4', 0],
             'btc_buy_tinkoff': [14, bybit_btc_buy_tinkoff, 'M5', 0],
             'btc_sell_tinkoff': [15, bybit_btc_sell_tinkoff, 'M6', 0]}

        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.price_class = 'price-amount'
        self.refresh_button_class = 'by-button trade-list-search-filter' \
                                    '__search-button by-inline-child ' \
                                    'by-button--outlined by-button--primary'

        for variant in self.data.keys():
            self.driver.switch_to.new_window()
            self.get_url(self.data[variant][1])

    def get_url(self, url):
        try:
            try:
                self.driver.get(url)
            except:
                try:
                    self.driver.get(url)
                except:
                    self.driver.get(url)
        except:
            return

    def refresh_tab(self):
        for variant in self.data.keys():
            self.driver.window_handles[self.data[variant][0]]
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            self.wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 f"//*[contains(@class, '{self.refresh_button_class}')]"))).click()

    def get_info(self):
        self.refresh_tab()
        for variant in self.data.keys():
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            self.data[variant][-1] = self.wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, self.price_class))).text

    def print_data(self):
        for variant in self.data.keys():
            print(self.data[variant][-1])

    def click_by_class(self, class_name):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(@class, '{class_name}')]")))
        self.driver.execute_script("arguments[0].click();", button)

    def click_by_text(self, text):
        button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(text(), '{text}')]")))
        self.driver.execute_script("arguments[0].click();", button)

    def click_by_class_index(self, class_name, i):
        button = self.driver.find_elements(By.XPATH,
                                           f"//*[contains(@class, '{class_name}')]")[
            i]
        self.driver.execute_script("arguments[0].click();", button)

    def click_by_text_index(self, text, i):
        button = \
            self.driver.find_elements(By.XPATH,
                                      f"//*[contains(text(), '{text}')]")[
                i]
        self.driver.execute_script("arguments[0].click();", button)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Активирует безоконный режим
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        f'--user-data-dir={bybit_user_path}')  # активирует данные гугла

    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver.exe',
                              options=options)

    bybit = BybitChecker(driver=driver)
    print(time.time())
    bybit.get_info()
    print(time.time())
    bybit.get_info()
    print(time.time())
    bybit.print_data()
