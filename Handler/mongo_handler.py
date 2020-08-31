import yaml
from tqdm import tqdm
from pymongo import MongoClient
from pymongo import UpdateOne
from Utils.utils import Log
yaml.warnings({'YAMLLoadWarning': False})

with open("config.yaml", "rt", encoding="utf-8") as stream:
    CONFIG = yaml.load(stream)['StockCrawler']


class MongoHandler:
    def __init__(self):
        self.log = Log(MongoHandler)
        conn = MongoClient(CONFIG['DB_ip'], CONFIG['DB_port'])

        self.save_collection = conn[CONFIG['DB_name']][CONFIG['save_collection_name']]
        self.target_collection = conn[CONFIG['DB_name']][CONFIG['target_collection_name']]
        self.log.info("MongoDB save collection {0}, target collection. - {1}".format(
            self.save_collection, self.target_collection
        ))

    def get_company(self):
        query = {}
        category_info = list(self.target_collection.find(query))
        return category_info

    def update_stock_data(self, stock_df):
        updates = []

        for idx, row in tqdm(stock_df.iterrows(), total=len(stock_df)):
            updates.append(
                UpdateOne(
                    {'Date': row['Date'], 'Code': row['Code']}, {'$set': {
                        'Company': row['Company']
                        , 'Type': row['Type']
                        , '3D-SMA': row['3D-SMA']
                        , '5D-SMA': row['5D-SMA']
                        , 'High-EMA': row['High-EMA']
                        , 'Low-EMA': row['Low-EMA']
                        , 'Code': row['Code']
                        , 'Date': row['Date']
                        , 'High': row['High']
                        , 'Low': row['Low']
                        , 'Open': row['Open']
                        , 'Close': row['Close']
                        , 'Volume': row['Volume']
                        , 'Adj Close': row['Adj Close']
                    }}, upsert=True
                )
            )

        self.log.debug("update list count- {0}".format(len(updates)))
        self.save_collection.bulk_write(updates)

    def add_stock_data(self, stock_df):
        self.save_collection.insert_many(stock_df.to_dict('records'))