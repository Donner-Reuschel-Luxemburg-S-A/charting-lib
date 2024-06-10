import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.opus_source import OpusSource
import matplotlib.dates as mdates

from charting.model.chart import Chart
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
from charting.transformer.ytd import Ytd

opus = OpusSource()
blp = BloombergSource()
observation_start = datetime.date(2023, 7, 1)
observation_end = datetime.date(2024, 5, 31)
id = '74185'
name = '6318 Gottorf-Fonds - D&R'

query = f"""
    SELECT
        reportings.report_date,
        accountsegments.nav
    FROM
        reportings
            JOIN
        accountsegments ON (accountsegments.reporting_uuid = reportings.uuid)
    WHERE
        accountsegments.accountsegment_id = '{id}'
            AND reportings.newest = 1
            AND reportings.report = 'positions'
            AND reportings.report_date BETWEEN '{observation_start.strftime('%Y-%m-%d')}' and '{observation_end.strftime('%Y-%m-%d')}'
"""

df = opus.read_sql(query=query)
df.set_index('report_date', inplace=True)
df.index = pd.to_datetime(df.index)

if __name__ == '__main__':
    # S&P Sector Performance
    """
    indices = ["S5ENRS Index", "S5CONS Index", "S5UTIL Index", "S5HLTH Index", "S5TELS Index", "S5MATR Index",
               "S5INDU Index", "S5COND Index", "S5FINL Index", "S5INFT Index", "S5RLST Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d')) for idx in indices]

    names = ["Energy", "Consumer Staples", "Utilities", "Health Care", "Communication Services", "Materials",
             "Industrials", "Consumer Discretionary", "Financials", "IT", "Real Estate"]

    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"S&P 500 Sector Performance"

    chart = Chart(title=title, filename="us_spx_sector_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="Percentage Points", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(2))

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))
    chart.plot()
    """

    # Stoxx 600 Sector Performance
    indices = ["SXEGR Index", "SX3GR Index", "SXDGR Index", "SXTGR Index", "SXPGR Index", "SXIGR Index", "SXMGR Index",
               "SXQGR Index", "SXKGR Index", "SX4GR Index", "SX7GR Index", "SX6GR Index", "SXAGR Index", "SXNGR Index",
               "SXOGR Index", "SXFGR Index", "SXRGR Index", "SX8GR Index", "SX86GR Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d')) for idx in indices]

    names = ["Oil & Gas", "Food & Beverage", "Health Care", "Travel", "Basic Resources", "Insurance", "Media",
             "Product & Households", "Telecom", "Chemicals", "Banks", "Utilities", "Autos & Parts", "Industrials",
             "Construction & Materials", "Financial Services", "Retail", "Technology", "Real Estate"]
    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"Stoxx Euro 600 Sector Performance"

    chart = Chart(title=title, filename="eu_sxxp_sector_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="Percentage Points", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(2))

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    chart.plot()

    # Indices Performance
    df1, t1 = blp.get_series(series_id='SX5E Index', field="px_close_1d", observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d'))
    df2, t2 = blp.get_series(series_id='SXXP Index', field="px_close_1d", observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d'))
    df3, t3 = blp.get_series(series_id='DAX Index', field="px_close_1d", observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d'))
    df4, t4 = blp.get_series(series_id='SPX Index', field="px_close_1d", observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d'))
    df5, t5 = blp.get_series(series_id='MXEF Index', field="px_close_1d", observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d'))

    title = "Euro Stoxx 50, Stoxx Euro 600, DAX, S&P 500, Emerging Markets - Performance"

    chart = Chart(title=title, filename="indices_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    major_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())
    chart.add_series(x=df5.index, y=df5['y'], label=t5, transformer=Ytd())

    chart.add_horizontal_line()
    chart.add_last_value_badge(2)

    chart.legend(ncol=3)
    chart.plot()


    start = (datetime.datetime.now().date() - datetime.timedelta(days=365))
    stock_indices = ["SPX Index", "NDX Index", "RTY Index", "SXXP Index", "SX5E Index", "DAX Index", "NKY Index",
                     "HSI Index"]
    stock_dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d')) for idx in stock_indices]
    stock_names = ["S&P 500", "NASDAQ 100", "Russell 2000", "Stoxx Europe 600", "Euro Stoxx 50", "DAX 40", "Nikkei 225",
                   "Hang Seng"]
    stock_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in stock_dfs]
    stock_data = sorted(zip(stock_names, stock_yields), key=lambda x: x[1])
    stock_data = list(zip(*stock_data))

    cmdty_indices = ["XBTUSD Curncy", "XAG Curncy", "XAU Curncy", "CL1 Comdty", "EURUSD Curncy", "USDJPY Curncy",
                     "EURCHF Curncy", "EURGBP Curncy"]
    cmdty_dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d')) for idx in
                 cmdty_indices]
    cmdty_names = ["Bitcoin USD", "Silver USD", "Gold USD", "Crude Oil WTI", "EUR/USD", "USD/JPY", "EUR/CHF", "EUR/GBP"]
    cmdty_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in cmdty_dfs]
    cmdty_data = sorted(zip(cmdty_names, cmdty_yields), key=lambda x: x[1])
    cmdty_data = list(zip(*cmdty_data))

    fi_indices = ["ER00 Index", "LEATTREU Index", "IBXXDECT Index", "IBOXXMJA Index", "JPEIHDEU Index"]
    fi_dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime('%Y%m%d'),
                                      observation_end=observation_end.strftime('%Y%m%d')) for idx in
              fi_indices]
    fi_names = ["Euro Corporate", "Euro-Aggregate: Treasury", "Covered Bonds", "EUR Liquid High Yield",
                "EMBI Global Core"]
    fi_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in fi_dfs]
    fi_data = sorted(zip(fi_names, fi_yields), key=lambda x: x[1])
    fi_data = list(zip(*fi_data))

    title = f"Global Asset Class Performance"

    chart = Chart(title=title, filename="global_asset_class_performance_last_year.png", num_rows=3)

    chart.configure_y_axis(y_axis_index=0, label="", row_index=0)
    chart.configure_y_axis(y_axis_index=0, label="", row_index=1)
    chart.configure_y_axis(y_axis_index=0, label="", row_index=2)

    chart.configure_x_axis(label="Percentage Points", minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(20))

    chart.add_series(stock_data[0], stock_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in stock_dfs), t_max=max(df.index.max() for df, _ in stock_dfs),
                     row_index=0)

    chart.add_series(fi_data[0], fi_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in fi_dfs), t_max=max(df.index.max() for df, _ in fi_dfs),
                     row_index=1)

    chart.add_series(cmdty_data[0], cmdty_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in cmdty_dfs), t_max=max(df.index.max() for df, _ in cmdty_dfs),
                     row_index=2)
    chart.plot()

    """
    # Marktausblick
    start = datetime.datetime.today().date() - relativedelta(years=10)

    #Global Indices P/E Overview
    indices = ["DAX Index", "SXXP Index", "SX5E Index", "SPX Index", "NDX Index", "INDU Index", "NKY Index",
               "MXEF Index", "UKX Index"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start=start.strftime("%Y%m%d")) for idx in indices]

    names = [title for _, title in dfs]
    y = [df["y"].values for df, _ in dfs]

    title = f"Global Indices P/E Overview"

    chart = Chart(title=title, filename="global_indices_per_overview.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    chart.plot()

    # SXXP vs. SPX P/E Ratio
    df1, t1 = blp.get_series(series_id='SXXP Index', field="RR900", observation_start=start.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SPX Index', field="RR900", observation_start=start.strftime("%Y%m%d"))

    title = "Stoxx Euro 600 & S&P 500 Price-Earnings Ratio"

    chart = Chart(title=title, filename="eu_us_sxxp_spx_pe_ratio.png")

    chart.configure_y_axis(y_axis_index=0, label="P/E", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(2))

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=2)
    major_formatter = mdates.DateFormatter("%y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Avg(offset=DateOffset(months=1)))

    chart.legend(ncol=2)
    chart.plot()
    
    # Quarterly Earnings SXXP
    df1, t1 = blp.get_series(series_id='SXXP Index', field="RR906", observation_start=start.strftime("%Y%m%d"))

    title = "Quarterly Stoxx Euro 600 Earnings Per Share"

    chart = Chart(title=title, filename="eu_sxxp_profits_quarterly.png", num_y_axis=2)

    chart.configure_y_axis(y_axis_index=1, label="EUR €", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(5))

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(10),
                           major_locator=MultipleLocator(20))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], chart_type='bar', transformer=[Resample('Q'), Pct(periods=4)], label=t1,
                     y_axis_index=0)

    df1 = df1[df1.index >= pd.Timestamp(start + relativedelta(years=1))]

    chart.add_series(x=df1.index, y=df1['y'], transformer=Resample('Q'), label=t1, y_axis_index=1)
    chart.add_horizontal_line(y_axis_index=0)
    chart.add_last_value_badge()

    chart.legend(ncol=2)
    chart.plot()


    # SXXP Profit MArgin
    df1, t1 = blp.get_series(series_id='SXXP Index', field="RR836", observation_start=start.strftime("%Y%m%d"))

    title = "Stoxx Euro 600 Profit Margin"

    chart = Chart(title=title, filename="eu_sxxp_profit_margin.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(0.25),
                           major_locator=MultipleLocator(1))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Avg(offset=DateOffset(months=1)))
    chart.add_last_value_badge()

    chart.legend(ncol=2)
    chart.plot()
    

    start = datetime.datetime.today().date() - relativedelta(years=10)

    df1, t1 = blp.get_series(series_id='GDBR10 Index', observation_start=start.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SX5E Index', field="RR907", observation_start=start.strftime("%Y%m%d"))
    df = df2 - df1

    title = "Euro Stoxx 50 Earning Yields minus Germany Government Bonds 10-Year "

    chart = Chart(title=title, filename="eu_euro_stoxx_profit_minus_ten_year_profit.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(0.5),
                           major_locator=MultipleLocator(1))

    minor_locator = mdates.MonthLocator(interval=3)
    major_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df.index, y=df['y'], label="SX5E Index Earning Yields - GDBR10 Index")

    chart.legend(ncol=2)
    chart.plot()
    """

