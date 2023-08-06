from datetime import datetime
import os
import time

from datetime import timedelta
import pandas as pd

import goquantdata


def get_price(client,
              ids=list(),
              start_date=datetime.now(),
              end_date=datetime.now()):
    db_dir = client.db_dir + "/raw/"
    if not os.path.exists(db_dir):
        raise goquantdata.exceptions.InputError("can't find db dir %s, please run build bd first" % db_dir)
    df = pd.DataFrame()
    today = start_date
    while today < end_date:
        file_path = "%s/%s.csv" % (db_dir, today.strftime("%Y%m%d"))
        if os.path.exists(file_path):
            cur_df = pd.read_csv(file_path)
            cur_df = cur_df[cur_df['symbol'].isin(ids)]
            df = df.append(cur_df)
        today += timedelta(days=1)
    df.reset_index(drop=True, inplace=True)
    return df

if __name__ == "__main__":
    from os.path import expanduser
    from goquantdata.local.client import Client
    client = Client(db_dir=expanduser("~") + '/data/localdb/')
    start_time = time.time()

    ids = ["AAPL", "AMD", "601228.XSHG"]
    start_date = datetime(2018, 1, 11, 0, 0)
    end_date = datetime(2018, 1, 15, 0, 0)
    df = get_price(client=client,
                   ids=ids,
                   start_date=start_date,
                   end_date=end_date)
    print(df)
    print("--- %s seconds ---" % (time.time() - start_time))
