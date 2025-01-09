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

    start_date = "20210801"

    blp = BloombergSource()

# ------------------------ DOWNLOAD DATA ---------------------------------

    # X variables

    # German
    ger_manu_df,  ger_manu_title = blp.get_series(series_id="MPMIDEMA Index",field="PX_LAST", observation_start=start_date)
    ger_serv_df, ger_serv_title = blp.get_series(series_id="MPMIDESA Index", field="PX_LAST", observation_start=start_date)

    # French
    fr_manu_df, fr_manu_title = blp.get_series(series_id="MPMIFRMA Index", field="PX_LAST", observation_start=start_date)
    fr_serv_df, fr_serv_title = blp.get_series(series_id="MPMIFRSA Index", field="PX_LAST", observation_start=start_date)

    # Japan
    jp_manu_df, jp_manu_title = blp.get_series(series_id="MPMIJPMA Index", field="PX_LAST", observation_start=start_date)
    jp_serv_df, jp_serv_title = blp.get_series(series_id="MPMIJPSA Index", field="PX_LAST", observation_start=start_date)

    # Australia
    aus_manu_df, aus_manu_title = blp.get_series(series_id="MPMIAUMA Index", field="PX_LAST", observation_start=start_date)
    aus_serv_df, aus_serv_title = blp.get_series(series_id="MPMIAUSA Index", field="PX_LAST", observation_start=start_date)

    # UK
    uk_manu_df, uk_manu_title = blp.get_series(series_id="MPMIGBMA Index", field="PX_LAST", observation_start=start_date)
    uk_serv_df, uk_serv_title = blp.get_series(series_id="MPMIGBSA Index", field="PX_LAST", observation_start=start_date)

    # US Regional Fed Survey
    us_empire_df, us_empire_title = blp.get_series(series_id="EMPRGBCI Index", field="PX_LAST", observation_start=start_date)
    us_philly_outlook_df, us_philly_outlook_title = blp.get_series(series_id="OUTFGAF Index", field="PX_LAST", observation_start=start_date)
    us_philly_serv_df, us_philly_serv_title = blp.get_series(series_id="PNMARADI Index", field="PX_LAST",  observation_start=start_date)
    us_chicago_act_df, us_chicago_act_title = blp.get_series(series_id="CFNAI Index", field="PX_LAST",  observation_start=start_date)
    us_ny_serv_df, us_ny_serv_title = blp.get_series(series_id="NYBLCNBA Index", field="PX_LAST", observation_start=start_date)

    # Dollar
    us_usd_df, us_usd_title = blp.get_series(series_id="USTWBGD  Index", field="PX_LAST", observation_start=start_date)
    us_usd_df.resample("ME")

    # Y variable

    # US PMIs
    us_manu_df, us_manu_title = blp.get_series(series_id="MPMIUSMA Index", field="PX_LAST", observation_start=start_date)
    us_serv_df, us_serv_title = blp.get_series(series_id="MPMIUSSA Index", field="PX_LAST", observation_start=start_date)

    # ------------------------ MERGE ---------------------------------


    merge=us_manu_df
    merge = pd.merge(merge, us_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv']
    merge = pd.merge(merge, ger_manu_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv','Ger_Manu']
    merge = pd.merge(merge, ger_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu','Ger_Serv']
    merge = pd.merge(merge, fr_manu_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv','Fr_Manu']
    merge = pd.merge(merge, fr_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu','Fr_Serv']
    merge = pd.merge(merge, jp_manu_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv','Jp_Manu']
    merge = pd.merge(merge, jp_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu','Jp_Serv']
    merge = pd.merge(merge, aus_manu_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv','Aus_Manu']
    merge = pd.merge(merge, aus_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv', 'Aus_Manu', 'Aus_Serv']
    merge = pd.merge(merge, uk_manu_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv', 'Aus_Manu', 'Aus_Serv', 'Uk_Manu']
    merge = pd.merge(merge, uk_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv', 'Aus_Manu', 'Aus_Serv', 'Uk_Manu','Uk_Serv']
    merge = pd.merge(merge, us_empire_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv','US_Empire']
    merge = pd.merge(merge, us_philly_outlook_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv', 'US_Empire','US_Philly_Outlook']
    merge = pd.merge(merge, us_philly_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv', 'US_Empire', 'US_Philly_Outlook','US_Philly_Serv']
    merge = pd.merge(merge, us_chicago_act_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv', 'US_Empire', 'US_Philly_Outlook', 'US_Philly_Serv','US_Chicago_Act']
    merge = pd.merge(merge, us_ny_serv_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv', 'US_Empire', 'US_Philly_Outlook', 'US_Philly_Serv',
                     'US_Chicago_Act','US_NY_Serv']
    merge = pd.merge(merge, us_usd_df, how='inner', left_index=True, right_index=True)
    merge.columns = ['US_Manu', 'US_Serv', 'Ger_Manu', 'Ger_Serv', 'Fr_Manu', 'Fr_Serv', 'Jp_Manu', 'Jp_Serv',
                     'Aus_Manu', 'Aus_Serv', 'Uk_Manu', 'Uk_Serv', 'US_Empire', 'US_Philly_Outlook', 'US_Philly_Serv',
                     'US_Chicago_Act', 'US_NY_Serv','US_USD']

    # monate = 12
    # merge['Wages']=merge['Wages'].shift(1)
    # merge['M2'] = merge['M2'].shift(18)
    # merge['Gasoline'] = transform_data(merge['Gasoline'], monate)
    # merge['NatGas'] = transform_data(merge['NatGas'], monate)
    # merge['MXN'] = transform_data(merge['MXN'], monate)

    merge = merge.dropna()

    # ------------------------ TRANSFORM ---------------------------------



    #est = smf.ols(formula='CPI ~ 0+JPY+CNY', data=merge).fit()
    est_manu = smf.ols(formula='US_Manu ~ 0+Uk_Manu+Aus_Manu',data=merge).fit()
    print(est_manu.summary())

    est_serv = smf.ols(formula='US_Serv ~ 0+Jp_Serv+US_NY_Serv', data=merge).fit()
    print(est_serv.summary())

    last_uk_serv = [(uk_serv_df['y'].iloc[-1])]
    last_jp_serv = [(jp_serv_df['y'].iloc[-1])]
    last_ny_serv = [(us_ny_serv_df['y'].iloc[-1])]



    Xnew_manu = pd.DataFrame({'Uk_Manu':last_uk_manu,'Aus_Manu':last_aus_manu})
    print(est_manu.predict(Xnew_manu))

    #Xnew_serv = pd.DataFrame({'Uk_Serv': last_uk_serv, 'Jp_Serv': last_jp_serv})
    Xnew_serv = pd.DataFrame({'US_NY_Serv': last_ny_serv, 'Jp_Serv': last_jp_serv})

    print(est_serv.predict(Xnew_serv))

    model = est_manu.predict()

    title = "US PMI Manu Model"
    #title = "Euro Unternehmensanleihen: Refinanzierungskosten"
    #metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_pmi_model_fit.png",num_y_axis=1)

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=2)
    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="%")

    chart.add_series(merge.index, merge['US_Manu'], label="PMI")
    chart.add_series(merge.index, model, label="Model")

    chart.legend(ncol=1)
    chart.plot()





if __name__ == '__main__':
    main()
