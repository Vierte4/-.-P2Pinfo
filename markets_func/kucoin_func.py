import os
import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.config import tinkoff_words, rosbank_words, kucoin_user_path, \
    bybit_user_path
from start import start_webdriver
from data.urls import *





row_class = 'ant-table-row  ant-table-row-level-0'
bank_transfer_src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAwCAYAAABXAvmHAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAMKADAAQAAAABAAAAMAAAAADbN2wMAAAEXElEQVRoBdWaPWgUQRTH38xuzsslUQ/xM8QIRlQU8SNiI6iFIlhoGiut1DpoISIKAS3EQklloyAoFjaaNhYq2ohRREEEIxjjV1SMenoJl+yO77/Hnnu5y+7cebvZG0h2dufNvN+bnZmdee8E1SAdHR5utL+qnaTUDkVqlSDqUIrSQqgWNK+UyAhBo4poUJB4RULclfPFnYttbWP/q551VZdOPB9Kj0/YexluL4PtYsxUZS2JLCvvZyP7kg2y79y69tHK6uelKzagZ+BjalTmjpGtjjO408PVKPbWYYgMSXE+bScu9HQuyXrLgvLaBtxUynj49N0hoVQPD5PFQQ1XU87D65MSomfrxqVX9gth6bShZcDRZ8OttmXdVkp16jT6vzJCiAFpGPsurm/7ENRWoAHdA8NbiKxbYfX6dIB4G0RGV29n26PpZPBc+hV2Pxk6oMi6FzU8mKATusHgxzjtG3DglX3Nr3JUZULIg72b2q+X01fWAAwbWM/9kCxXKfpnYlyQsb3ccCoxwJmwk9bjmRg2fh2DOSFNY/PUiV00B7BUOqtNSMukH2BQGToUbGD0yhYZgHU+qqXSC6GbBxsYvfKFIeR8YSk3GLeh44VFHkMpTYkO94tdeAPYHsQdHgaA0dnK4IaT8wawMRvL2UO12tvkmw7vP0NnGhOyHRtAE2qcXaXGxmzXojm0beFsajaL5lHNSH9PWnR/5Bf1f/7p2yY6GswsdNUZQtgS+9bgwpUtSdrTmg4NHvrRMdABXUHJZZY4jOT38/5V2ptm+QvUsFRHF5jBbjonKY3DiOQjFZLNR60wE/S4uvz1qBTYTRwD/QX/lb74kaXLb778exBC7vDyBfqtMrvkZWmVfo14SYJd8sDoiBeWPg3YTXgPdKus4NXh+OoluuJVyc2bZdL7bE6rLthNuD5052XSkNSaSmg1HoUQ2AtbiSgUhqFDwukURsNRtAl2LLlVOZSiAAzSAXaTP0uDLBjJSmTxZLvx9lsJ19q5KdqQbip5HvQA7Cbvr1/xero7SLgW5VgsBr7/KWlqbsKsygCwSzhaS1qslwfMbsJLbI0I9kdW6pyt3EqDvzwn15R+R5qMarbnIgt2CRc3t9sfhJOz7SCRwHJ2GdLCZKLkr7mh2AAdXWAGu/MdgIs7SPvLn2OESRh2gg7oCkous3Mig3+ej5QZxpvWXf55fIIuvR6hrfNbQjvU4ET24GuGoMsvce9nwAwZzudT99O3p5Stzrj3cb4KKU73blx2FoyFrQSCC3BZxBkcbI5bhVldzoIB8LMguOAWxPUKRtcnBMaCAbhBZATBBeTjmMAGRi9bkQEI6yAyEsehBCawTQ09FRkAy/LeX6OLR9u419KZzYPF6JrqmQZTiQF4CD88v64jyMchgaVcbABsZQ1AASIiiIzM7JvgwIZPdAache8AbsqluAf5Ag2AUXUdZnXfSl0Hul0jcK3bnxp4jUC+bn/sMdUQ3M/kz23+AkTn23kGX0d5AAAAAElFTkSuQmCC'


class KucoinChecker():
    def __init__(self, driver: webdriver.Chrome):
        self.data = \
            {'usdt_buy_rosbank': [8, kucoin_buy_usdt_url, 'D10',0],
             'usdt_buy_tinkoff': [8, kucoin_buy_usdt_url, 'D12',0],
             'usdt_sell_rosbank': [9, kucoin_sell_usdt_url, 'D11',0],
             'usdt_sell_tinkoff': [9, kucoin_sell_usdt_url, 'D13',0],
             'btc_buy_rosbank': [10, kucoin_buy_btc_url, 'E10',0],
             'btc_buy_tinkoff': [10, kucoin_buy_btc_url, 'E12',0],
             'btc_sell_rosbank': [11, kucoin_sell_btc_url, 'E11',0],
             'btc_sell_tinkoff': [11, kucoin_sell_btc_url, 'E13',0]}
        self.data_list = list(self.data.keys())

        self.driver = driver
        self.wait = WebDriverWait(driver, 5)
        self.price_class = 'width210 price average mr-40'
        self.close_button_class = 'closeWrapper___5HLi-'
        self.refresh_button_text = 'Настройка обновления'
        self.methods_button_text = 'Все способы'
        self.accept_button_text = 'Подтвердить'
        self.refresh_time_text = 'Обновится через 5s'
        self.fcking_window_class = 'video-close ivu-icon ivu-icon-md-close'
        self.action_button_class = 'optBtn___1gAZq'
        self.next_button_class = ' ant-pagination-next'
        self.description_class = 'adsContent___aLlQm'
        self.price_class = 'emphasisTxt'
        self.warning_class = 'ant-message-notice'
        self.open_urls()

    def open_urls(self):
        # Открываем каждый вариант в новом окне
        for variant in self.data_list[::2]:
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
        for variant in self.data_list[::2]:
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            self.driver.refresh()

    def get_info(self):
        # self.refresh_tab()
        for variant in self.data_list[::2]:
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])

            tinkoff_price = None
            rosbank_price = None
            buttons = self.driver.find_elements(By.CLASS_NAME, self.action_button_class)


            # Прокликивает кажду кнопку, ждёт появления кнопки закрытия окна
            # с подробной информацией, ищет в окне ключевые слова, если они есть,
            # сохраняет цену, после поиска жмёт на крестик
            for button in buttons:
                button.click()

                try:
                    close_button = self.wait.until(EC.element_to_be_clickable(
                        (By.XPATH, f"//*[contains(@class, '{self.close_button_class}')]")))
                except Exception as e:
                    continue

                description = self.driver.find_element(By.CLASS_NAME,
                                                  self.description_class).text.lower()

                if not tinkoff_price:
                    for word in tinkoff_words:
                        if word in description:
                            tinkoff_price = self.driver.find_element(
                                By.CLASS_NAME,
                                self.price_class).text
                            self.save_tinkoff(variant, tinkoff_price)

                if not rosbank_price:
                    for word in rosbank_words:
                        if word in description:
                            rosbank_price = self.driver.find_element(
                                By.CLASS_NAME,
                                self.price_class).text
                            self.save_rosbank(variant, rosbank_price)

                close_button.click()

                if tinkoff_price and rosbank_price:
                    break


    def save_rosbank(self, variant, rosbank_price):
        self.data[variant][-1] = rosbank_price

    def save_tinkoff(self, variant, tinkoff_price):
        variant = variant.replace('rosbank', 'tinkoff')
        self.data[variant][-1] = tinkoff_price

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
        button = self.driver.find_elements(By.XPATH, f"//*[contains(@class, '{class_name}')]")[i]
        self.driver.execute_script("arguments[0].click();", button)

    def click_by_text_index(self, text, i):
        button = self.driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")[i]
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
                              options=options, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'])

    binance = KucoinChecker(driver=driver)
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.print_data()