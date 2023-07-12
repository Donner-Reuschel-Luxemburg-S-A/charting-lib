import matplotlib.dates as mdates
import pandas as pd
from pandas import DataFrame, DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Country, Category
from charting.transformer.avg import Avg
from charting.transformer.resample import Resample
from examples import fred

if __name__ == '__main__':
    df = pd.read_excel('data/bankruptcy_data.xlsx', parse_dates=True, index_col="Date")
    df = DataFrame({'count': df.groupby("Date").size()}, index=df.index)

    d2, t2 = fred.get_series(series_id='JHDUSRGDPBR')

    title = "US Weekly Bankruptcies"

    metadata = Metadata(title=title, country=Country.US, category=Category.CREDIT)
    chart = Chart(title=title, metadata=metadata, filename="us_weekly_bankruptcy.png")

    chart.configure_y_axis(y_axis_index=0, label="Number of Bankruptcies")

    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=4)
    major_formatter = mdates.DateFormatter("%Y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(df.index, df['count'], label='Number of bankruptcies', transformer=[Resample(rule='W', resampler='sum'), Avg(offset=DateOffset(weeks=4))])
    chart.add_series(df.index, df['count'], label='Number of bankruptcies', transformer=[Resample(rule='W', resampler='sum'), Avg(offset=DateOffset(weeks=12))])

    chart.add_vertical_line(x=d2.index, y=d2["y"], label="US Recession")

    chart.legend(ncol=2)
    chart.plot()
