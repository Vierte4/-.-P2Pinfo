import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.config import bybit_user_path
from data.urls import *


class BinanceChecker():
    def __init__(self, driver: webdriver.Chrome):
        self.data = \
            {'usdt_buy_rosbank': [0, binance_usdt_buy_rosbank, 'D3', 0],
             'usdt_sell_rosbank': [1, binance_usdt_sell_rosbank, 'D4', 0],
             'usdt_buy_tinkoff': [2, binance_usdt_buy_tinkoff, 'D5', 0],
             'usdt_sell_tinkoff': [3, binance_usdt_sell_tinkoff, 'D6', 0],
             'btc_buy_rosbank': [4, binance_btc_buy_rosbank, 'E3', 0],
             'btc_sell_rosbank': [5, binance_btc_sell_rosbank, 'E4', 0],
             'btc_buy_tinkoff': [6, binance_btc_buy_tinkoff, 'E5', 0],
             'btc_sell_tinkoff': [7, binance_btc_sell_tinkoff, 'E6', 0]}

        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.price_class = 'css-1m1f8hn'
        self.refresh_button_class = ' css-qev57u'
        self.refresh_time_text = '5 с до обновления'
        self.fcking_window_class = 'css-1pcqseb'
        self.data_keys_list = list(self.data.keys())

        self.get_url(self.data[self.data_keys_list[0]][1])
        for variant in self.data_keys_list[1:]:
            self.driver.switch_to.new_window()
            self.get_url(self.data[variant][1])
        self.refresh_tab()

    def close_fcking_window(self):
        x = self.driver.find_elements(By.XPATH,
                                      f"//*[contains(@class, '{self.fcking_window_class}')]")
        if x:
            x[0].click()

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
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            self.close_fcking_window()
            self.click_by_class(self.refresh_button_class)
            self.click_by_text(self.refresh_time_text)

    def get_info(self):
        for variant in self.data.keys():
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            element = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"//*[contains(@class, '{self.price_class}')]")))

            self.data[variant][-1] = element.text

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
        self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")[
            i]
        self.driver.execute_script("arguments[0].click();", button)


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Активирует безоконный режим
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        f'--user-data-dir={bybit_user_path}')  # активирует данные гугла
    options.add_argument(f'--ssl-protocol=any')
    options.add_argument(f'--ignore-ssl-errors=true')

    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver.exe',
                              options=options,
                              service_args=['--ignore-ssl-errors=true',
                                            '--ssl-protocol=any'])

    binance = BinanceChecker(driver=driver)
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.print_data()

'''def binance_checker(initial_url, driver: webdriver.Chrome):
    try:
        try:
            driver.get(initial_url)
        except:
            try:
                driver.get(initial_url)
            except:
                driver.get(initial_url)
        wait = WebDriverWait(driver, 30)

        return wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, price_class))).text
    except Exception as e:
        print(e)
        return 'Ошибка'

def binance_thread(driver):
    # driver = start_webdriver(binance_user_path)


    usdt_buy_rosbank = binance_checker(binance_usdt_buy_rosbank, driver)
    usdt_sell_rosbank = binance_checker(binance_usdt_sell_rosbank, driver)
    usdt_buy_tinkoff = binance_checker(binance_usdt_buy_tinkoff, driver)
    usdt_sell_tinkoff = binance_checker(binance_usdt_sell_tinkoff, driver)
    btc_buy_rosbank = binance_checker(binance_btc_buy_rosbank, driver)
    btc_sell_rosbank = binance_checker(binance_btc_sell_rosbank, driver)
    btc_buy_tinkoff = binance_checker(binance_btc_buy_tinkoff, driver)
    btc_sell_tinkoff = binance_checker(binance_btc_sell_tinkoff, driver)

    print(usdt_buy_rosbank)
    print(usdt_sell_rosbank)
    print(usdt_buy_tinkoff)
    print(usdt_sell_tinkoff)
    print(btc_buy_rosbank)
    print(btc_sell_rosbank)
    print(btc_buy_tinkoff)
    print(btc_sell_tinkoff)
    print(4444)

'''
