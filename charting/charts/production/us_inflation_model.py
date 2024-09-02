import pandas as pd
import statsmodels.formula.api as smf
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region


def transform_data(t, k):
    return (t-t.shift(k))/t.shift(k)


def main(**kwargs):

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
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="us_inflation_model_fit", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.configure_y_axis(label="PERCENTAGE POINTS")

    chart.add_series(merge.index, merge['CPI'], label="Inflation")
    chart.add_series(merge.index, model, label="Model")

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')


