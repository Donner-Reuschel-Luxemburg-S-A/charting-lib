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

    df1, t1 = blp.get_series(series_id='MXEF Index', field="px_close_1d", observation_start=start.strftime("%Y%m%d"))

    title = "MSCI Emerging Markets Yield"

    metadata = Metadata(title=title, region=Region.EM, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="em_mxef_yield_six_month.png")

    chart.configure_y_axis(y_axis_index=0, label="%", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2))

    major_locator = mdates.MonthLocator(interval=1)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label=t1, transformer=Ytd())
    chart.add_horizontal_line()

    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
