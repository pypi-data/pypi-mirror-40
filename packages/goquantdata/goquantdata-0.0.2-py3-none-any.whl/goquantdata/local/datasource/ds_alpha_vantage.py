import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from .datasource import DataSource


class AlphaVantage(DataSource):
    RENAME_COL = {'1. open': 'open',
                  '2. high': 'high',
                  '3. low': 'low',
                  '4. close': 'close',
                  '5. volume': 'volume',
                  'date': 'date'}

    def __init__(self, api_key):
        self.api_key = api_key
        DataSource.__init__(self, name=__name__)

    def connect(self):
        self.ts = TimeSeries(key=self.api_key, output_format='pandas', indexing_type='date')

    def get_daily(self, start_date, end_date, ids, market):
        if market=='us' or market=='cn':
            ret = self._get_daily(start_date, end_date, ids)
        else:
            self.logger("market type %s is not support"%market)
        return ret

    def _get_daily(self, start_date, end_date, ids):
        ret = pd.DataFrame()
        for i in range(len(ids)):
            self.logger.info("downloading...%s, %d/%d" % (ids[i], i, len(ids)))
            df, meta_data = self.ts.get_daily(symbol=ids[i], outputsize='full')
            df.rename(columns=self.RENAME_COL, inplace=True)
            df['date'] = pd.to_datetime(df.index, format='%Y-%m-%d')
            df.set_index('date', inplace=True, drop=False)
            df = df.loc[(df.index >= start_date) & (df.index <= end_date)]
            df['symbol'] = ids[i]
            ret = pd.concat([ret, df], axis=0)
        ret.sort_values(by='date', inplace=True)
        return ret


