import random
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import tinkoff_words, rosbank_words, kucoin_user_path
from start import start_webdriver
from urls import *

action_button_class = 'optBtn___1gAZq'
close_button_class = 'closeWrapper___5HLi-'
next_button_class = ' ant-pagination-next'
description_class = 'adsContent___aLlQm'
price_class = 'emphasisTxt'
warning_class = 'ant-message-notice'


def kucoin_checker(initial_url, driver: webdriver.Chrome):
    try:
        driver.get(initial_url)
    except:
        try:
            driver.get(initial_url)
        except:
            driver.get(initial_url)

    tinkoff_price = None
    rosbank_price = None
    wait = WebDriverWait(driver, 30)

    # Собирает все кнопки купить/продать, нажатие которых выводит
    # окно с подробной информацией
    wait.until(EC.element_to_be_clickable(
        (By.CLASS_NAME, action_button_class)))
    buttons = driver.find_elements(By.CLASS_NAME, action_button_class)

    # Прокликивает далее 5 раз в случае ненахождения какой-то информации
    for a in range(5):

        # Прокликивает кажду кнопку, ждёт появления кнопки закрытия окна
        # с подробной информацией, ищет в окне ключевые слова, если они есть,
        # сохраняет цену, после поиска жмёт на крестик
        for button in buttons:
            button.click()

            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, close_button_class)))

            close = driver.find_elements(By.CLASS_NAME, close_button_class)

            if len(close) == 0:
                continue

            close_button = close[0]
            description = driver.find_element(By.CLASS_NAME,
                                              description_class).text.lower()

            if not tinkoff_price:
                for word in tinkoff_words:
                    if word in description:
                        tinkoff_price = driver.find_element(By.CLASS_NAME,
                                                            price_class).text
                        break

            if not rosbank_price:
                for word in rosbank_words:
                    if word in description:
                        rosbank_price = driver.find_element(By.CLASS_NAME,
                                                            price_class).text
                        break

            close_button.click()
            if tinkoff_price and rosbank_price:
                return tinkoff_price, rosbank_price

        wait.until(EC.element_to_be_clickable(
            (By.LINK_TEXT, 'Далее'))).click()

    return tinkoff_price, rosbank_price


def kucoin_thread():
    driver = start_webdriver(kucoin_user_path)

    while True:
        usdt_buy_tinkoff, usdt_buy_rosbank = kucoin_checker(kucoin_buy_usdt_url, driver)
        usdt_sell_tinkoff, usdt_sell_rosbank = kucoin_checker(kucoin_sell_usdt_url, driver)
        btc_buy_tinkoff, btc_buy_rosbank = kucoin_checker(kucoin_buy_btc_url, driver)
        btc_sell_tinkoff, btc_sell_rosbank = kucoin_checker(kucoin_sell_btc_url, driver)
        print(usdt_buy_rosbank)
        print(usdt_sell_rosbank)
        print(usdt_buy_tinkoff)
        print(usdt_sell_tinkoff)
        print(btc_buy_rosbank)
        print(btc_sell_rosbank)
        print(btc_buy_tinkoff)
        print(btc_sell_tinkoff)
        print(2222)

        time.sleep(random.randint(40, 60))