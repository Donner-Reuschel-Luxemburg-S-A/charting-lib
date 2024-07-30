import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.api import OLS
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def main():

    start_date = "20200101"

    blp = BloombergSource()


    xb1_df, xb1_title = blp.get_series(series_id="XB1 Comdty",field="PX_LAST", observation_start=start_date)

    cl1_df, cl1_title = blp.get_series(series_id="CL1 Comdty",field="CHG_PCT_1M", observation_start=start_date)

    manu_df, manu_title = blp.get_series(series_id="NAPMPRIC INDEX",field="PX_LAST", observation_start=start_date)
    serv_df, serv_title = blp.get_series(series_id="NAPMNPRC INDEX", field="PX_LAST", observation_start=start_date)
    atl_df, atl_title = blp.get_series(series_id="WGTRMDWG INDEX", field="PX_LAST", observation_start=start_date)
    gdp_df, gdp_title = blp.get_series(series_id="EHGDUSY INDEX", field="PX_LAST", observation_start=start_date)
    m2_df, m2_title = blp.get_series(series_id="M2% YOY INDEX", field="PX_LAST", observation_start=start_date)
    dxy_df, dxy_title = blp.get_series(series_id="DXY CURNCY", field="PX_LAST", observation_start=start_date)
    ng_df, ng_title = blp.get_series(series_id="NG1 Comdty", field="PX_LAST", observation_start=start_date)

    mxn_df, mxn_title = blp.get_series(series_id="USDMXN CURNCY", field="CHG_PCT_1M", observation_start=start_date)
    eur_df, eur_title = blp.get_series(series_id="USDEUR CURNCY", field="CHG_PCT_1M", observation_start=start_date)
    jpy_df, jpy_title = blp.get_series(series_id="USDJPY CURNCY", field="CHG_PCT_1M", observation_start=start_date)
    cny_df, cny_title = blp.get_series(series_id="USDCNY CURNCY", field="CHG_PCT_1M", observation_start=start_date)
    cad_df, cad_title = blp.get_series(series_id="USDCAD CURNCY", field="CHG_PCT_1M", observation_start=start_date)

    inf_df, inf_title = blp.get_series(series_id="IMP1CHNG Index", field="PX_LAST", observation_start=start_date)

    title = "US Inflation Model"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_model.png",num_y_axis=2,num_rows=4)

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title,y_axis_index=0,row_index=0)
    chart.add_series(m2_df.index, m2_df['y'], label=m2_title,transformer=[Lag(offset=DateOffset(months=-12))],y_axis_index=1,row_index=0)

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0,row_index=1)
    chart.add_series(atl_df.index, atl_df['y'], label=atl_title, y_axis_index=1,row_index=1)

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=2)
    chart.add_series(manu_df.index, manu_df['y'], label=manu_title, y_axis_index=1, row_index=2)

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title, y_axis_index=0, row_index=2)
    chart.add_series(serv_df.index, serv_df['y'], label=serv_title, y_axis_index=1, row_index=2)

    chart.legend(ncol=1)
    chart.plot()

    inf_df['y'] = inf_df['y']/100

    merge = pd.merge(inf_df, manu_df, how='inner', left_index=True, right_index=True)

    merge = pd.merge(merge, serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services']
    m2_df=m2_df.shift(12)
    merge = pd.merge(merge, m2_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services','M2']
    atl_df=atl_df.shift(1)
    merge = pd.merge(merge, atl_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2','Wages']
    merge = pd.merge(merge, xb1_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline']
    merge = pd.merge(merge, cl1_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline','Oil']

    merge = pd.merge(merge,mxn_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline','Oil','MXN']
    merge = pd.merge(merge, eur_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline','Oil', 'MXN','EUR']
    merge = pd.merge(merge, jpy_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline', 'Oil','MXN', 'EUR','JPY']
    merge = pd.merge(merge, cny_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline', 'Oil','MXN', 'EUR', 'JPY','CNY']
    merge = pd.merge(merge, cad_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'Manufacturing', 'Services', 'M2', 'Wages', 'Gasoline', 'Oil','MXN', 'EUR', 'JPY', 'CNY','CAD']

    #merge = merge - merge.shift(1)
    merge = merge.dropna()

    est = smf.ols(formula='CPI ~ 0+JPY+CNY', data=merge).fit()
    #est = smf.ols(formula='CPI ~ 0+Manufacturing+Services+M2+Wages+Gasoline+DXY',data=merge).fit()
    print(est.summary())

    df_model = inf_df
    df_model['y'] = 0.02 * merge['CPI'] + 0.025 * merge['Manufacturing']+0.1 * merge['M2'] + 0.13 * merge['Wages'] + 0.004 * merge['Gasoline']
    df_model = df_model.dropna()

    title = "US Inflation Model fitted"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inflation_model_fit.png",num_y_axis=2)

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(inf_df.index, inf_df['y'], label=inf_title,y_axis_index=0)
    chart.add_series(df_model.index, df_model['y'], label="Model",y_axis_index=1)

    chart.legend(ncol=1)
    chart.plot()

if __name__ == '__main__':
    main()
