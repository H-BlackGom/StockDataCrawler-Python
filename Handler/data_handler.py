import yaml
import types
import pandas as pd
from Handler.mongo_handler import MongoHandler
from Utils.utils import Log
yaml.warnings({'YAMLLoadWarning': False})
with open("config.yaml", "rt", encoding="utf-8") as stream:
    CONFIG = yaml.load(stream)['StockCrawler']


class DataHandler:
    def __init__(self):
        self.log = Log(DataHandler)
        self.mongo = MongoHandler()
        self.company_info = None
        self.company_list = None

        check_target_location = CONFIG['company_name_location']
        if check_target_location == 'DB':
            self.get_target_company = types.MethodType(self._get_company_by_mongo, self)
        elif check_target_location == 'File':
            self.get_target_company = types.MethodType(self._get_company_by_file, self)

    def get_target_company(self):
        pass

    def save_stock_data(self, stock_df):
        if CONFIG['iterate']:
            self.mongo.update_stock_data(stock_df)
        else:
            self.mongo.add_stock_data(stock_df)

    def _get_company_by_mongo(self, obj):
        self.log.debug("Get company information by database(MongoDB)")
        self.company_info = pd.DataFrame(self.mongo.get_company())
        self.company_list = self.company_info[['company', 'code']]

    def _get_company_by_file(self, obj):
        pass
