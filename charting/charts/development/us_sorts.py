import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.api import OLS
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from statsmodels.tsa.stattools import adfuller
from source_engine.bloomberg_source import BloombergSource
from xbbg import blp
import datetime

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def compute_quantiles(df):
    return 0


def get_constituents(index_ticker):
    fields = ['INDX_MEMBERS']
    df = blp.bds(index_ticker, fields)
    return df


def get_data(equity_ticker, fields, start_date):
    df = blp.bdh(equity_ticker, fields, start_date, Per='M')
    return df

def downloadandsave():
    tickers = ['SPX Index']
    fields = ['INDX_MEMBERS']
    start_date = datetime.date(2014, 12, 31)

    df = get_constituents("SPX Index")
    ticker_list = df['member_ticker_and_exchange_code'].to_list()

    fundamental_field_list = ['PX_LAST', 'RETURN_ON_INV_CAPITAL', 'RETURN_COM_EQY', 'EBIT_TO_NET_SALES',
                              'T12_FCF_MARGIN', 'SALES_3YR_AVG_GROWTH', 'SALES_5YR_AVG_GR', 'BASIC_EPS_3YR_AVG_GROWTH',
                              'BASIC_EPS_5YR_AVG_GR', 'INTEREST_COVERAGE_RATIO', 'TOT_DEBT_TO_TOT_EQY']
    technical_field_list = ['LAST_CLOSE_TRR_3MO', 'LAST_CLOSE_TRR_6MO', 'LAST_CLOSE_TRR_1YR', 'CHG_PCT_MOV_AVG_50D',
                            'CHG_PCT_MOV_AVG_100D', 'CHG_PCT_MOV_AVG_200D', 'CHG_PCT_HIGH_52WEEK', 'RSI_14D',
                            'PUT_CALL_VOLUME_RATIO_CUR_DAY', 'SKEW_MONEYNESS_SPREAD']
    risk_field_list = ['VOLATILITY_30D', 'VOLATILITY_260D', 'VOLATILITY_162W', 'IVOL_MID', 'EQY_RAW_BETA',
                       'EQY_BETA_STD_DEV_ERR_6M', 'BEST_PE_RATIO', 'PX_TO_SALES_RATIO', 'PX_TO_BOOK_RATIO',
                       'BEST_CUR_EV_TO_EBITDA']

    t = ['A UN Equity']

    df_final = get_data(t, "PX_LAST", start_date)

    for ticker in ticker_list:
        df2 = get_data(ticker + " Equity", "PX_LAST", start_date)
        df_final = pd.concat([df_final, df2], axis=1).ffill().bfill()

    for ticker in ticker_list:
        for field in fundamental_field_list:
            df2 = get_data(ticker + " Equity", field, start_date)
            df_final = pd.concat([df_final, df2], axis=1).ffill().bfill()

    df_final.to_excel('Daten-All.xlsx')


if __name__ == '__main__':


