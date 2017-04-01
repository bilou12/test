import datetime
from pprint import pprint

from yahoo_finance import Share

import pandas as pd

import matplotlib.pyplot as plt

if __name__ == '__main__':
    yahoo = Share('YHOO')

    # get simple information
    print(yahoo.get_open())
    print(yahoo.get_price())
    print(yahoo.get_trade_datetime())

    yahoo.refresh()
    print(yahoo.get_price())
    print(yahoo.get_trade_datetime())

    print(yahoo.get_volume())
    print(yahoo.get_dividend_share())
    print(yahoo.get_dividend_yield())
    print(yahoo.get_50day_moving_avg())

    pprint(yahoo.get_historical('2017-01-01', datetime.datetime.today().strftime('%Y-%m-%d')))

    # display historical graph of Yahoo
    historicals = (yahoo.get_historical('2017-01-01', datetime.datetime.today().strftime('%Y-%m-%d')))
    result_df = pd.DataFrame(data=historicals)
    result_df.set_index('Date')
    result_df['Close'] = result_df['Close'].astype(float)
    plots = result_df[['Close', 'Date']].plot(x='Date', y='Close')
    plt.show()