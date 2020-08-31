import time
import random
import yaml
import pandas as pd
import numpy as np
import pandas_datareader as pdr
from datetime import datetime
from tqdm import tqdm
from Crawlers.crawler import Crawler
yaml.warnings({'YAMLLoadWarning': False})

with open("config.yaml", "rt", encoding="utf-8") as stream:
    CONFIG = yaml.load(stream)['StockCrawler']


class StockCrawler(Crawler):
    def __init__(self, data_handler):
        super().__init__(StockCrawler)
        self.data_handler = data_handler

    def _get_date(self):
        now_date = datetime.now()
        s_date = now_date.strftime('%Y-%m-%d')
        e_date = now_date.strftime('%Y-%m-%d')
        self.log.debug("start date - {0}, end date - {1}".format(s_date, e_date))

        return s_date, e_date

    def execute_crawler(self, company_df):
        self.log.info("Execute get stock data crawler")

        stock_df = pd.DataFrame()
        if CONFIG['iterate']:
            start_date, end_date = self._get_date()
        else:
            start_date = CONFIG['start_date']
            end_date = CONFIG['end_date']

        for idx, row in tqdm(company_df.iterrows(), total=len(company_df)):
            try:
                company = row.company
                code = row.code

                tmp_df = pdr.DataReader(code, "yahoo", start_date, end_date)
                tmp_df.reset_index(inplace=True)
                tmp_df['Company'] = company
                tmp_df['Type'] = tmp_df.apply(lambda x: int(x['Close'] > x['Open']), axis=1)
                tmp_df['3D-SMA'] = tmp_df['Close'].rolling(window=3, min_periods=1).mean()
                tmp_df['5D-SMA'] = tmp_df['Close'].rolling(window=5, min_periods=1).mean()
                tmp_df['High-EMA'] = pd.Series.ewm(tmp_df['High'], span=1).mean()
                tmp_df['Low-EMA'] = pd.Series.ewm(tmp_df['Low'], span=1).mean()
                tmp_df['Code'] = code

                stock_df = pd.concat([stock_df, tmp_df])
                time.sleep(random.randrange(1, 3))
            except KeyError:
                self.log.warning("KeyError: 'Date' - Stop trading company - {0}".format(company))
                stop_stock_data = {
                    'Date': datetime.strptime(start_date, "%Y-%m-%d"),
                    'High': np.NaN,
                    'Low': np.NaN,
                    'Open': np.NaN,
                    'Close': np.NaN,
                    'Volume': np.NaN,
                    'Adj Close': np.NaN,
                    'Company': company,
                    'Type': np.NaN,
                    'Code': code
                }
                tmp_df = pd.DataFrame(data=stop_stock_data, index=[0])
                tmp_df.reset_index(inplace=True)
                stock_df = pd.concat([stock_df, tmp_df])
                time.sleep(random.randrange(1, 3))
                continue

        stock_df.drop(['index'], axis=1, inplace=True)
        stock_df.reset_index(inplace=True)
        stock_df.drop(['index'], axis=1, inplace=True)

        self.data_handler.save_stock_data(stock_df)
