import pandas as pd
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def find_key(input_dict, value):
    for key in input_dict.keys():
        if value in input_dict[key]:
            return key
    for key in input_dict.keys():
        if not value in input_dict[key]:
            return value

def get_html(url):
    data1 = pd.read_html(url, skiprows=2)[0]
    df = pd.DataFrame(data1)
    df.columns=['Date', 'Unit', 'Rate']
    df.loc[:,'Date'] = pd.to_datetime(df['Date'])

    engine = create_engine('sqlite:///current.db', echo=True)
    sqlite_connection = engine.connect()

    sqlite_table = 'table'
    df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
    sqlite_connection.close()

def main():
    url_dict = 'https://cbr.ru/eng/currency_base/dynamics/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    response = requests.get(url=url_dict, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    codes = soup.find_all('option')
    data = dict()
    for code in codes:
        name = code['value']
        value = code.text.strip()
        data[name] = value
    val = input("Enter currency, like Euro, US Dollar full list on https://cbr.ru/eng/currency_base/daily/: ")
    currency = find_key(data, val)
    today = datetime.today().strftime('%d/%m/%Y')
    url = 'https://cbr.ru/eng/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=' + currency + '&UniDbQuery.From=01/07/1992&UniDbQuery.To=' + today
    get_html(url)

main()















