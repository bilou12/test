import datetime
import urllib.request

import pandas as pd
from bs4 import BeautifulSoup
from pandas.tseries.offsets import BDay
from pandas_highcharts import core
from yahoo_finance import Share


class IndexParser:
    def __init__(self, index, start_date, end_date):
        self.dic_index = {'CAC40': {'url': 'https://en.wikipedia.org/wiki/CAC_40#Composition',
                                    'col_ticker': 0,
                                    'col_sector': 2},
                          'SMI': {'url': 'https://en.wikipedia.org/wiki/Swiss_Market_Index#Constituents',
                                  'col_ticker': 3,
                                  'col_sector': 1}}
        if index in self.dic_index.keys():
            self.site = self.dic_index[index]['url']
            self.col_ticker = self.dic_index[index]['col_ticker']
            self.col_sector = self.dic_index[index]['col_sector']
            self.start_date = start_date
            self.end_date = end_date
            self.headers = {'User-Agent': 'Mozilla/5.0'}
            self.sector_tickers = dict()
            self.results = list()
            self.result_df = None
            self.chart = None
            self.scrape_index_list()
            self.download_data()
            # self.make_json_highcharts()
        else:
            print('Index not in list')

    def scrape_index_list(self):
        req = urllib.request.Request(self.site, headers=self.headers)
        page = urllib.request.urlopen(req)
        soup = BeautifulSoup(page)

        table = soup.find('table', {'class': 'wikitable sortable'})
        for row in table.findAll('tr'):
            col = row.findAll('td')
            if len(col) > 0:
                sector = str(col[self.col_sector].string.strip()).lower().replace(' ', '_')
                ticker = str(col[self.col_ticker].string.strip())
                if sector not in self.sector_tickers:
                    self.sector_tickers[sector] = list()
                self.sector_tickers[sector].append(ticker)

    def download_data(self):
        for sector, tickers in self.sector_tickers.items():
            print('Downloading data from Yahoo for %s sector' % sector)
            for ticker in tickers:
                share = Share(ticker)
                price = share.get_price()
                adv = share.get_avg_daily_volume()
                data = {'ticker': ticker, 'sector': sector, 'price': price, 'adv': adv}
                self.results.append(data)
        self.result_df = pd.DataFrame(self.results)

        print('Finished downloading data')

    def make_json_highcharts(self):
        self.chart = core.serialize(df=self.results, render_to='my-chart', output_type='json')


if __name__ == '__main__':
    index_parser = IndexParser(index='CAC40',
                               start_date=datetime.datetime.today() + BDay(-1),
                               end_date=datetime.datetime.today() + BDay(-1))
