import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from data.config import bybit_user_path
from data.urls import *

price_class = 'width210 price average mr-40'
methods_button_text = 'Все способы'
accept_button_text = 'Подтвердить'
white_space_class = 'otc-header-auto flex-between noPing'
fcking_window_class = 'video-close ivu-icon ivu-icon-md-close'


class HuobiChecker():
    def __init__(self, driver: webdriver.Chrome):
        self.data = \
            {'usdt_buy_rosbank': [0, huobi_buy_usdt_url, 'Росбанк', 'L10', 0],
             'usdt_sell_rosbank': [1, huobi_sell_usdt_url, 'Росбанк', 'L11', 0],
             'usdt_buy_tinkoff': [2, huobi_buy_usdt_url, 'Тинькофф', 'L12', 0],
             'usdt_sell_tinkoff': [3, huobi_sell_usdt_url, 'Тинькофф', 'L13',
                                   0],
             'btc_buy_rosbank': [4, huobi_buy_btc_url, 'Росбанк', 'M10', 0],
             'btc_sell_rosbank': [5, huobi_sell_btc_url, 'Росбанк', 'M11', 0],
             'btc_buy_tinkoff': [6, huobi_buy_btc_url, 'Тинькофф', 'M12', 0],
             'btc_sell_tinkoff': [7, huobi_sell_btc_url, 'Тинькофф', 'M13', 0]}

        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.price_class = 'width210 price average mr-40'
        self.refresh_button_text = 'Настройка обновления'
        self.methods_button_text = 'Все способы'
        self.accept_button_text = 'Подтвердить'
        self.refresh_time_text = 'Обновится через 5s'
        self.fcking_window_class = 'video-close ivu-icon ivu-icon-md-close'

        self.open_urls()

    def open_urls(self):
        a = False
        # Открываем каждый вариант в новом окне
        for variant in self.data.keys():
            if a:
                self.driver.switch_to.new_window()
            a = True
            self.get_url(self.data[variant][1])
            self.close_fcking_window()

            # Выбираем отслеживаемый банк
            try:
                self.click_by_text(self.methods_button_text)
            except:
                self.click_by_text(self.methods_button_text)

            time.sleep(1)

            self.click_by_text(self.data[variant][2])
            self.click_by_text_index(self.accept_button_text, -1)

            # Включаем автоматическое обновление котировок раз в 5 сек.
            self.click_by_text(self.refresh_button_text)
            self.click_by_text(self.refresh_time_text)

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
            self.driver.refresh()

    def get_info(self):
        # self.refresh_tab()
        for variant in self.data.keys():
            self.driver.switch_to.window(
                self.driver.window_handles[self.data[variant][0]])
            self.data[variant][-1] = self.wait.until(EC.element_to_be_clickable(
                (
                By.XPATH, f"//*[contains(@class, '{self.price_class}')]"))).text

    def print_data(self):
        for variant in self.data.keys():
            print(self.data[variant][2])

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

    binance = HuobiChecker(driver=driver)
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.get_info()
    print(time.time())
    binance.print_data()

'''def huobi_checker(initial_url, driver:webdriver.Chrome):
    action = webdriver.ActionChains(driver)
    try:
        driver.get(initial_url)
    except:
        try:
            driver.get(initial_url)
        except:
            driver.get(initial_url)

    wait = WebDriverWait(driver, 30)

    # Выбираем тинькофф
    try:
        methods_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(text(), '{methods_button_text}')]")))
        methods_button.click()
    except:
        methods_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//*[contains(text(), '{methods_button_text}')]")))
        methods_button.click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), 'Тинькофф')]"))).click()

    time.sleep(1)
    driver.find_elements(By.XPATH, f"//*[contains(text(), '{accept_button_text}')]")[-1].click()

    # Сохраняем лучшую цену фильтра Тинькофф
    tinkoff_price = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(@class, '{price_class}')]"))).text

    # Убираем тинькофф и выбираем Росбанк
    methods_button.click()
    time.sleep(2)
    tink_button = driver.find_elements(By.XPATH, f"//*[contains(text(), 'Тинькофф')]")[1]
    tink_button.click()
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), 'Росбанк')]"))).click()
    time.sleep(1)

    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), '{accept_button_text}')]")))
    driver.find_elements(By.XPATH, f"//*[contains(text(), '{accept_button_text}')]")[-1].click()
    time.sleep(1)

    rosbank_price = wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(@class, '{price_class}')]"))).text

    # Возвращаем "Все способы"
    methods_button.click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), 'Все способы')]"))).click()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"//*[contains(text(), '{accept_button_text}')]")))
    driver.find_elements(By.XPATH,
                         f"//*[contains(text(), '{accept_button_text}')]")[
        -1].click()
    time.sleep(1)

    return tinkoff_price, rosbank_price


def huobi_thread(driver):
    # driver = start_webdriver(huobi_user_path)

    try:
        usdt_buy_tinkoff, usdt_buy_rosbank = huobi_checker(
            huobi_buy_usdt_url, driver)
    except Exception as e:
        usdt_buy_tinkoff, usdt_buy_rosbank = 'Ошибка', 'Ошибка'
        print(e)

    try:
        usdt_sell_tinkoff, usdt_sell_rosbank = huobi_checker(
            huobi_sell_usdt_url, driver)
    except Exception as e:
        usdt_sell_tinkoff, usdt_sell_rosbank = 'Ошибка', 'Ошибка'
        print(e)

    try:
        btc_buy_tinkoff, btc_buy_rosbank = huobi_checker(
            huobi_buy_btc_url, driver)
    except Exception as e:
        btc_buy_tinkoff, btc_buy_rosbank = 'Ошибка', 'Ошибка'
        print(e)
    try:
        btc_sell_tinkoff, btc_sell_rosbank = huobi_checker(
            huobi_sell_btc_url, driver)
    except Exception as e:
        btc_sell_tinkoff, btc_sell_rosbank = 'Ошибка', 'Ошибка'
        print(e)

    print(usdt_buy_rosbank)
    print(usdt_sell_rosbank)
    print(usdt_buy_tinkoff)
    print(usdt_sell_tinkoff)
    print(btc_buy_rosbank)
    print(btc_sell_rosbank)
    print(btc_buy_tinkoff)
    print(btc_sell_tinkoff)
    print(1111)'''
