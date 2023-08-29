import matplotlib.dates as mdates
from pandas import DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
from charting import fred

def main():
    title = "US retail sales: YoY change"

    d1, t1 = fred.get_series(series_id='RSAFS', observation_start="2020-01-01")

    metadata = Metadata(title=title, region=Region.US, category=Category.CONSUMER)
    chart = Chart(title=title, metadata=metadata, filename="us_retail_sales_yoy.png")

    minor_locator = mdates.MonthLocator(interval=1)
    major_locator = mdates.MonthLocator(interval=3)
    major_formatter = mdates.DateFormatter(fmt="%m/%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.configure_y_axis(y_axis_index=0, label="%", y_lim=(0, 35))

    chart.add_series(x=d1.index, y=d1['y'], label=t1, chart_type='bar', bar_bottom=0,
                     transformer=[Pct(periods=12), Avg(offset=DateOffset(months=3))])

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()

