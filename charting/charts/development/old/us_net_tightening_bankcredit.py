import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.transformer.pct import Pct
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg

if __name__ == '__main__':
    fred = FredSource()
    chart = Chart(title="US Bank Credit", num_rows=1, num_y_axis=2,
                  filename="us_tightening_bankcredit.png")

    d0, t0 = fred.get_series(series_id='DRTSCILM', observation_start="1992-01-01")
    d1, t1 = fred.get_series(series_id='TOTCI', observation_start="1992-01-01")

    chart.configure_y_axis(row_index=0, y_axis_index=0)

    major_locator = mdates.YearLocator(base=5)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)


    chart.add_series(d1.index, d1["y"], row_index=0, label=t0,transformer=Pct(periods=52),y_axis_index=1)
    chart.add_series(d0.index, d0["y"], row_index=0, label=t0, transformer=Lag(offset=DateOffset(months=-12)))

    chart.add_last_value_badge()
    chart.legend(ncol=2)
    chart.plot()
