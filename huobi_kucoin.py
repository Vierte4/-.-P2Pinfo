import random
import time

from data.config import kucoin_user_path
from google_table import append_to_sheet
from markets_func import KucoinChecker, HuobiChecker
from start import start_webdriver


class MainParser():
    def __init__(self, user_data_path):
        self.driver = start_webdriver(user_data_path)
        self.user_data_path = user_data_path

        # Порядок инициации парсеров имеет значение
        self.huobi = HuobiChecker(self.driver)
        self.kucoin = KucoinChecker(self.driver)

    def parse(self):
        self.huobi.get_info()
        self.kucoin.get_info()
        kucoin_data = self.kucoin.data
        huobi_data = self.huobi.data
        for key in kucoin_data.keys():
            append_to_sheet(kucoin_data[key][-1], kucoin_data[key][-2])
        for key in huobi_data.keys():
            append_to_sheet(huobi_data[key][-1], huobi_data[key][-2])

    def parsing(self):
        while True:
            try:
                self.parse()
            except Exception as e:
                self.driver.quit()
                self.driver = start_webdriver(self.user_data_path)
                self.huobi = HuobiChecker(self.driver)
                self.kucoin = KucoinChecker(self.driver)
                continue
            time.sleep(random.randint(40, 60))


if __name__ == '__main__':
    print('OPEN URL START', time.time())
    parser = MainParser(kucoin_user_path)
    parser.parsing()
