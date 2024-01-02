import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
from charting.transformer.resample import Resample
from charting.transformer.ytd import Ytd


def main():
    blp = BloombergSource()

    start = datetime.datetime.today().date() - relativedelta(months=6)

    df1, t1 = blp.get_series(series_id='SX5E Index', field="px_close_1d", observation_start=start.strftime("%Y%m%d"))
    df2, t2 = blp.get_series(series_id='SXXP Index', field="px_close_1d", observation_start=start.strftime("%Y%m%d"))
    df3, t3 = blp.get_series(series_id='MCXP Index', field="px_close_1d", observation_start=start.strftime("%Y%m%d"))
    df4, t4 = blp.get_series(series_id='SCXP Index', field="px_close_1d", observation_start=start.strftime("%Y%m%d"))

    title = "Euro Stoxx 50, Stoxx Euro 600, Stoxx Euro 200 Small & Mid Caps Yield"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxfivee_sxxp_mcxp_scxp_yield_six_month.png")

    chart.configure_y_axis(y_axis_index=0, label="%", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2))

    major_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_series(x=df2.index, y=df2['y'], label=t2, transformer=Ytd())
    chart.add_series(x=df3.index, y=df3['y'], label=t3, transformer=Ytd())
    chart.add_series(x=df4.index, y=df4['y'], label=t4, transformer=Ytd())

    chart.add_horizontal_line()

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
