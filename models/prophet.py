import pandas as pd
import numpy as np
import matplotlib.pylab as plt

import os

#prophet library
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
import plotly.offline as py
from dateutil.relativedelta import relativedelta


# this script extract data from yahoo finance website
# need to mention only stock company symbol only .
# this file contains historical share price of stock 
import pandas
from pandas_datareader import data, wb
import datetime
import urllib
import csv


YAHOO_TODAY="http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sd1ohgl1vl1"

# extarcting data from yahoo finance 

start = datetime.datetime.today() - relativedelta(years=5)
end = datetime.datetime.today()


def stock_extractor(stock):
    df = data.DataReader(stock, "yahoo", start="2014/1/1",end= end)
    return df.to_csv(f"./src/stock_price_{stock}.csv",index=True)


def chk_null(df):
    if df.isnull().values.any():
        print('Applying ffill on null values')
        return df.fillna(method='ffill',inplace=True)
    else:
        print('no null value')
        return df

def prophet_predict(stock):
    df_prophet = pd.read_csv(f'./src/stock_price_{stock}.csv',na_values=['NAN','null','nan','Null','N/A','n/a'])
    df_prophet.rename(columns={'Adj Close': 'y','Date':'ds'}, inplace=True)
    chk_null(df_prophet)

    df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
    df_prophet = df_prophet[['ds','y']]

    m = Prophet(changepoint_prior_scale=0.09)
    m.fit(df_prophet)

    from fbprophet.plot import plot_yearly
    m = Prophet(yearly_seasonality=20).fit(df_prophet)


    # making prediction for 365 days
    future = m.make_future_dataframe(periods=365)# make ts dataframe
    forecast = m.predict(future)# prediction


    return forecast.to_csv(f"./out/pred_prophet_{stock}.csv",index=True)



