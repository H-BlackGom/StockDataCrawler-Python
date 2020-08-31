import yaml
from Utils.utils import Log
from Handler.data_handler import DataHandler
from Crawlers.stock_crawler import StockCrawler
yaml.warnings({'YAMLLoadWarning': False})
with open("config.yaml", "rt", encoding="utf-8") as stream:
    CONFIG = yaml.load(stream)['StockCrawler']


if __name__ == '__main__':
    log = Log(__name__)

    data_handler = DataHandler()
    data_handler.get_target_company()

    crawler = StockCrawler(data_handler)
    crawler.execute_crawler(data_handler.company_list)
