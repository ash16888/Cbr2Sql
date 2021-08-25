"""#Script get exchange rates from cbr.ru to sqlite """
import pandas as pd
from sqlalchemy import create_engine
import requests
from bs4 import BeautifulSoup
import datetime


def curr_dict(url_list):
    """Make dictionary with list of currency and codes"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    response = requests.get(url=url_list, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    codes = soup.find_all('option')
    data = dict()
    for code in codes:
        name = code['value']
        value = code.text.strip()
        data[name] = value
    return data


def find_key(input_dict, value):
    """In dictionary find key attr to currency, if not quit"""
    for key in input_dict.keys():
        if value in input_dict[key]:
            return key
    for key in input_dict.keys():
        if not value in input_dict[key]:
            print("Please, try again  insert correct name")
            quit()


def get_sqlite(url, value, end_date):
    """ Get HTML Table to Pandas DataFrame than convert ti sqlite"""
    tab = pd.read_html(url, skiprows=2)[0]
    df = pd.DataFrame(tab)
    df.columns = ['Date', 'Unit', 'Rate']
    value = value.replace(' ', '').lower()
    end_date = end_date.replace('/', '')
    engine = create_engine('sqlite:///' + value + end_date + '.db', echo=True)
    sqlite_connection = engine.connect()
    sqlite_table = 'table'
    df.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
    sqlite_connection.close()


def main():
    """Main"""
    d = curr_dict('https://cbr.ru/eng/currency_base/dynamics/')
    value = input("Enter currency, like Euro, US Dollar full list on https://cbr.ru/eng/currency_base/daily/: ")
    curr_code = find_key(d, value)
    """Rates for tomorrow"""
    end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime('%d/%m/%Y')
    url = 'https://cbr.ru/eng/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.so=1&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=' + curr_code + '&UniDbQuery.From=01/07/1992&UniDbQuery.To=' + end_date
    get_sqlite(url, value, end_date)


main()







