import os

import matplotlib.dates as mdates
import pandas as pd
from pandas import DataFrame, DateOffset
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting.transformer.avg import Avg
from charting.transformer.resample import Resample


def main(**kwargs):
    fred = FredSource()
    excel_path = os.path.join(os.path.dirname(__file__), "data", "bankruptcy_data.xlsx")
    df = pd.read_excel(excel_path, parse_dates=True, index_col="Date")
    df = DataFrame({'count': df.groupby("Date").size()}, index=df.index)

    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')

    title = "US Weekly Bankruptcies"

    metadata = Metadata(title=title, region=Region.US, category=Category.CREDIT)
    chart = Chart(title=title, metadata=metadata, filename="us_weekly_bankruptcy.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="Number of Bankruptcies")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(df.index, df['count'], label='Number of bankruptcies',
                     transformer=[Resample(rule='W', resampler='sum'), Avg(offset=DateOffset(weeks=4))])
    chart.add_series(df.index, df['count'], label='Number of bankruptcies',
                     transformer=[Resample(rule='W', resampler='sum'), Avg(offset=DateOffset(weeks=12))])

    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)

    return chart.plot(bloomberg_source_override='BCY')


if __name__ == '__main__':
    main()
