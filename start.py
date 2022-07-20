import os

from selenium import webdriver


def start_webdriver(user_data_path):
    options = webdriver.ChromeOptions()

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument(
        f'--user-data-dir={user_data_path}')  # активирует данные гугла
    driver = webdriver.Chrome(executable_path=os.getcwd() + '/chromedriver.exe',
                              options=options)
    return driver
