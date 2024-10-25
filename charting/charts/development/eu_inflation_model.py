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

    # Natural Gas
    ng1_df, ng1_title = blp.get_series(series_id="TTFG1MON OECM Index",field="PX_LAST", observation_start=start_date)
    ng1_df=ng1_df.resample("ME").last()
    # Oil
    co1_df, co1_title = blp.get_series(series_id="CO1 Comdty",field="PX_LAST", observation_start=start_date)
    co1_df = co1_df.resample("ME").last()
    # Gasoline
    ve1_df, ve1_title = blp.get_series(series_id="VE1 Comdty", field="PX_LAST", observation_start=start_date)
    ve1_df = ve1_df.resample("ME").last()
    # Electricity
    eg1_df, eg1_title = blp.get_series(series_id="ELGAYR1 Index", field="PX_LAST", observation_start=start_date)
    eg1_df = eg1_df.resample("ME").last()


    # Indeed Wage Tracker
    wages_df, wages_title = blp.get_series(series_id="LNTWEMUY Index", field="PX_LAST", observation_start=start_date)
    # US GDP YOY
    #gdp_df, gdp_title = blp.get_series(series_id="EHGDUSY INDEX", field="PX_LAST", observation_start=start_date)
    # ECB M3 YOY
    m1_df, m1_title = blp.get_series(series_id="ECMAM1YY Index", field="PX_LAST", observation_start=start_date)
    m3_df, m3_title = blp.get_series(series_id="ECMAM3YY Index", field="PX_LAST", observation_start=start_date)

    # Fiscal

    budget_df, budget_title = blp.get_series(series_id="EUBDEURO Index", field="PX_LAST", observation_start=start_date)

    # Currencies

    usd_df, usd_title = blp.get_series(series_id="EURUSD CURNCY", field="PX_LAST", observation_start=start_date)
    usd_df = usd_df.resample("ME").last()

    chf_df, chf_title = blp.get_series(series_id="EURCHF CURNCY", field="PX_LAST", observation_start=start_date)
    chf_df = chf_df.resample("ME").last()


    # Y variable

    # Inflation
    inf_df, inf_title = blp.get_series(series_id="ECCPEMUY Index", field="PX_LAST", observation_start=start_date)

    # ------------------------ MERGE ---------------------------------


    merge=inf_df
    merge = pd.merge(merge, m1_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['CPI', 'm1']
    merge = pd.merge(merge, wages_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1','Wages']
    merge = pd.merge(merge, ng1_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages','NatGas']
    merge = pd.merge(merge, co1_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas','Oil']
    merge = pd.merge(merge, ve1_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil','Gasoline']
    merge = pd.merge(merge, chf_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil', 'Gasoline','CHF']
    merge = pd.merge(merge, eg1_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil', 'Gasoline', 'CHF','Electricity']
    merge = pd.merge(merge, usd_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil', 'Gasoline', 'CHF', 'Electricity','USD']
    merge = pd.merge(merge, budget_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil', 'Gasoline', 'CHF', 'Electricity', 'USD','Deficit']
    merge = pd.merge(merge, m3_df, how='left', left_index=True, right_index=True).ffill()
    merge.columns = ['CPI', 'm1', 'Wages', 'NatGas', 'Oil', 'Gasoline', 'CHF', 'Electricity', 'USD', 'Deficit','M3']

    monate = 12
    merge['Wages']=merge['Wages'].shift(1)
    merge['Deficit'] = merge['Deficit'].shift(1)
    merge['m1'] = merge['m1'].shift(18)
    merge['M3'] = merge['M3'].shift(18)
    merge['NatGas'] = transform_data(merge['NatGas'], monate)
    merge['Oil'] = transform_data(merge['Oil'], monate)
    merge['Gasoline'] = transform_data(merge['Gasoline'], monate)
    merge['CHF'] = transform_data(merge['CHF'], monate)
    merge['Electricity'] = transform_data(merge['Electricity'], monate)


    merge = merge.dropna()

    # ------------------------ TRANSFORM ---------------------------------



    est = smf.ols(formula='CPI ~ 0+m1+Wages+USD+Deficit+M3+Electricity',data=merge).fit()
    print(est.summary())
    model = est.predict()

    versatz = 12

    lastm1 = [m1_df['y'].iloc[-18]]
    lastm3 = [m3_df['y'].iloc[-18]]
    lastwages = [wages_df['y'].iloc[-1]]
    lastdeficit = [budget_df['y'].iloc[-1]]
    lasteg= [(eg1_df['y'].iloc[-1]-eg1_df['y'].iloc[-versatz])/eg1_df['y'].iloc[-versatz]]
    lastusd = [(usd_df['y'].iloc[-1] - usd_df['y'].iloc[-versatz]) / usd_df['y'].iloc[-versatz]]
    lastoil = [(co1_df['y'].iloc[-1] - co1_df['y'].iloc[-versatz]) / co1_df['y'].iloc[-versatz]]
    lastchf = [(chf_df['y'].iloc[-1] - chf_df['y'].iloc[-versatz]) / chf_df['y'].iloc[-versatz]]
    #lastgasoline = [(xb1_df['y'].tail(2)[0]-xb1_df['y'].tail(versatz)[0])/xb1_df['y'].tail(versatz)[0]]


    Xnew = pd.DataFrame({'Wages':lastwages,'USD':lastusd,'Deficit':lastdeficit,'M3':lastm3,'Electricity':lasteg,'m1':lastm1})
    print(est.predict(Xnew))



    title = "EU Inflation Model"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="eu_inflation_model_fit.png",num_y_axis=1)

    minor_locator = mdates.MonthLocator(interval=12)
    major_locator = mdates.MonthLocator(interval=24)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(merge.index, merge['CPI'], label="Inflation")
    chart.add_series(merge.index, model, label="Model")

    chart.legend(ncol=1)
    chart.plot()



if __name__ == '__main__':
    main()
