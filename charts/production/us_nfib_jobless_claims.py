import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from charting.model.chart import Chart
from charting import blp, fred

if __name__ == '__main__':
    #df1, t1 = blp.get_series(series_id='SBOIPRIC Index', observation_start='19950131')
    #df2, t2 = blp.get_series(series_id='CLEVCPIA Index', observation_start='19950131')
    df3, t3 = fred.get_series(series_id='JHDUSRGDPBR')

    title = "Small Business hiring plans point to higher jobless claims"
    #metadata = Metadata(title=title, region=Region.US, category=Category.EMPLOYMENT)

    chart = Chart(title=title, num_y_axis=2, filename="us_nfib_jobless_claims.png")

    chart.configure_y_axis(y_axis_index=0, label="Mio", minor_locator=MultipleLocator(50))
    chart.configure_y_axis(y_axis_index=1, label="%", y_lim=(-20, 30), reverse_axis=True, minor_locator=MultipleLocator(0.5))

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=12)
    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    #chart.add_series(x=df1.index, y=df1['y'], label=t1, y_axis_index=0, fill=True,
    #                 fill_threshold=-35, transformer=[Resample('M'), Lead(offset=DateOffset(months=10))])
    #chart.add_series(x=df2.index, y=df2['y'], label=t2, y_axis_index=1,  transformer=Resample('M'))
    chart.add_vertical_line(x=df3.index, y=df3["y"], label="US Recession")

    chart.legend()
    chart.plot()

