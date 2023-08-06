# GO Quant Data Client API v1
Build local csv database and get stock daily open, high, low, close, volume.
Client also support all original API function of quandl and jqdata.

version 0.0.2
## Install
```bash
pip install goquantdata
```
## Usage
#### Quick Start
Example 1. Build Local DB and Get symbol open, close, high, low, volume
```python
from datetime import datetime
import goquantdata
from os.path import expanduser
import goquantdata.local.private_config as cfg

client = goquantdata.LocalClient(db_dir=expanduser("~") + '/data/localdb/',
                key_quandl=cfg.CONFIG_QUANDL['api_key'],
                jq_password=cfg.CONFIG_JQDATA['password'],
                jq_username=cfg.CONFIG_JQDATA['username'])
start_date = datetime.strptime("20170102", "%Y%m%d")
end_date = datetime.strptime("20180102", "%Y%m%d")
client.build_db(start_date=start_date, end_date=end_date)
df = client.get_price(ids=["AAPL", "AMD", "601228.XSHG"],
                      start_date=start_date,
                      end_date=end_date)
```
Example 2. use original sdk function
To use original sdk function, for jqdata use "jq_{name of function}",
for quandl, use "ql_{name of function}"
```python
# use original sdk function
df = client.jq_get_price(security=["601228.XSHG"],
                          start_date=start_date,
                          end_date=end_date,
                          frequency='daily',
                          fields=None,
                          skip_paused=False,
                          fq='pre',
                          count=None)
```
## Output Format
- get_price return dataframe

| symbol      | date        | open        | high        | low         | close       | volume      | market |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |
| AAPL        | 2017-01-03  | 114.369701  | 114.893155  | 113.342546  | 114.715378  | 28781865.0  | us |

## Data Source
| Market      | Client Type | Universe | Source |
| ----------- | ----------- | ----------- | ----------- |
| cn stock    | local | xshg300 | [JQData](https://www.joinquant.com/help/api/help?name=Stock) |
| us stock  | local | sp500 | [Quandl/WIKI](https://www.quandl.com/tools/python) |

