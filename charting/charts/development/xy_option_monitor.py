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

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def transform_data(t,k):
    return (t-t.shift(k))/t.shift(k)


def main():

    start_date = "20040101"

    blp = BloombergSource()

# ------------------------ DOWNLOAD DATA ---------------------------------

    # X variables

    # Gasoline
    xb1_df, xb1_title = blp.get_series(series_id="XB1 Comdty",field="PX_LAST", observation_start=start_date)
    xb1_df=xb1_df.resample("ME").last()

    # Natural Gas
    ng1_df, ng1_title = blp.get_series(series_id="NG1 Comdty", field="PX_LAST", observation_start=start_date)
    ng1_df = ng1_df.resample("ME").last()

    # Atlanta Fed Wage Tracker
    atl_df, atl_title = blp.get_series(series_id="WGTRMDWG INDEX", field="PX_LAST", observation_start=start_date)

    # US M2 YOY
    m2_df, m2_title = blp.get_series(series_id="M2% YOY INDEX", field="PX_LAST", observation_start=start_date)

    # Currencies
    mxn_df, mxn_title = blp.get_series(series_id="USDMXN CURNCY", field="PX_LAST", observation_start=start_date)
    mxn_df = mxn_df.resample("ME").last()


    # Y variable

    # Inflation
    inf_df, inf_title = blp.get_series(series_id="CPI YOY Index", field="PX_LAST", observation_start=start_date)

    # ------------------------ MERGE ---------------------------------
    xb1_df.resample("ME")

    merge=inf_df
    merge = pd.merge(merge, m2_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'M2']
    merge = pd.merge(merge, atl_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'M2','Wages']
    merge = pd.merge(merge, xb1_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'M2', 'Wages', 'Gasoline']
    merge = pd.merge(merge, ng1_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'M2', 'Wages', 'Gasoline', 'NatGas']
    merge = pd.merge(merge,mxn_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'M2', 'Wages', 'Gasoline','NatGas','MXN']

    monate = 12
    merge['Wages']=merge['Wages'].shift(1)
    merge['M2'] = merge['M2'].shift(18)
    merge['Gasoline'] = transform_data(merge['Gasoline'], monate)
    merge['NatGas'] = transform_data(merge['NatGas'], monate)
    merge['MXN'] = transform_data(merge['MXN'], monate)


    merge = merge.dropna()

    # ------------------------ MODEL ---------------------------------


    est = smf.ols(formula='CPI ~ 0+M2+Wages+Gasoline+NatGas+MXN',data=merge).fit()
    print(est.summary())
    model = est.predict()


    # ----------------------- PREDICT OOS -----------------------------
    versatz = 12
    lastm2 = [m2_df['y'].iloc[-19]]
    lastwages = [atl_df['y'].iloc[-2]]
    lastgasoline = [(xb1_df['y'].iloc[-1]-xb1_df['y'].iloc[-versatz])/xb1_df['y'].iloc[-versatz]]
    lastgas = [(ng1_df['y'].iloc[-1] - ng1_df['y'].iloc[-versatz]) / ng1_df['y'].iloc[-versatz]]
    lastmxn = [(mxn_df['y'].iloc[-1] - mxn_df['y'].iloc[-versatz]) / mxn_df['y'].iloc[-versatz]]

    Xnew = pd.DataFrame({'M2':lastm2,'Wages':lastwages,'Gasoline':lastgasoline,'NatGas':lastgas,'MXN':lastmxn})
    print('New CPI Estimate:')
    print(est.predict(Xnew))

    # ----------------------- CHART -----------------------------

    title = "US Inflation Model"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_model_fit.png",num_y_axis=1)

    minor_locator = mdates.MonthLocator(interval=12)
    major_locator = mdates.MonthLocator(interval=24)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(merge.index, merge['CPI'], label="Inflation")
    chart.add_series(merge.index, model, label="Model")

    chart.legend(ncol=1)
    chart.plot()

    # ------------------------ CHARTS ---------------------------------

    title = "US Inflation: Money Supply & Wages"

    chart = Chart(title=title, filename="us_inflation_model_m2_atl.png", num_y_axis=2, num_rows=2)

    minor_locator = mdates.MonthLocator(interval=12)
    major_locator = mdates.MonthLocator(interval=48)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(m2_df.index, m2_df['y'], label=m2_title, transformer=[Lag(offset=DateOffset(months=-12))],y_axis_index=1, row_index=0)
    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=0)

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=1)
    chart.add_series(atl_df.index, atl_df['y'], label=atl_title, y_axis_index=1, row_index=1)

    chart.legend(ncol=1)
    chart.plot()

    title = "US Inflation: Gasoline & Natural Gas Prices"

    chart = Chart(title=title, filename="us_inflation_model_xb1_ng1.png", num_y_axis=2, num_rows=2)

    minor_locator = mdates.MonthLocator(interval=12)
    major_locator = mdates.MonthLocator(interval=48)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(xb1_df.index, xb1_df['y'], label=xb1_title, y_axis_index=1, row_index=0)
    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=0)

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=1)
    chart.add_series(ng1_df.index, ng1_df['y'], label=ng1_title, y_axis_index=1, row_index=1)

    chart.legend(ncol=1)
    chart.plot()


if __name__ == '__main__':
    main()
