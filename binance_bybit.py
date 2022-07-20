import random
import time

from data.config import binance_user_path
from google_table import append_to_sheet
from markets_func import BybitChecker, BinanceChecker
from start import start_webdriver


class MainParser():
    def __init__(self, user_data_path):
        self.driver = start_webdriver(user_data_path)
        self.user_data_path = user_data_path
        # Порядок инициации парсеров имеет значение
        self.binance = BinanceChecker(self.driver)
        self.bybit = BybitChecker(self.driver)

    def parse(self):
        self.bybit.get_info()
        self.binance.get_info()
        binance_data = self.binance.data
        for key in binance_data.keys():
            append_to_sheet(binance_data[key][-1], binance_data[key][-2])
        bybit_data = self.bybit.data
        for key in bybit_data.keys():
            append_to_sheet(bybit_data[key][-1], bybit_data[key][-2])

    def parsing(self):
        while True:
            try:
                self.parse()
            except Exception as e:
                self.driver.quit()
                self.driver = start_webdriver(self.user_data_path)
                self.binance = BinanceChecker(self.driver)
                self.bybit = BybitChecker(self.driver)
                continue
            time.sleep(random.randint(40, 60))


if __name__ == '__main__':
    print('OPEN URL START', time.time())
    parser = MainParser(binance_user_path)
    parser.parsing()
