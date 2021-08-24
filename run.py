import pandas as pd
from sqlalchemy import create_engine
url = 'https://cbr.ru/eng/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01235&UniDbQuery.From=01/07/1992&UniDbQuery.To=24/08/2021'

data = pd.read_html(url, skiprows=2)[0]

df = pd.DataFrame(data)
df.columns=['Date', 'Unit', 'Rate']
df.loc[:,'Date'] = pd.to_datetime(df['Date'])

engine = create_engine('sqlite:///usd.db', echo=True)
sqlite_connection = engine.connect()

sqlite_table = 'usd'
df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()
