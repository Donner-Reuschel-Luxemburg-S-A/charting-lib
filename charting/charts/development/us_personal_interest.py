import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from pandas import DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg
from charting.transformer.pct import Pct
from charting.transformer.invert import Invert

def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19600101"

    us_pi_df, us_pi_title = fred.get_series(series_id='B069RC1', observation_start=start_time)
    us_ave_df, us_ave_title = fred.get_series(series_id='CES0500000003', observation_start=start_time)




    title = "US Personal Interest Payments YoY"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_personal_interest.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=10), major_locator=mdates.YearLocator(base=10))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(10),label="%")

    chart.add_series(us_pi_df.index, us_pi_df['y'],transformer=[Pct(periods=6)], label=us_pi_title)
    #chart.add_series(us_ave_df.index,us_ave_df['y'], label=us_ave_title)


    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
