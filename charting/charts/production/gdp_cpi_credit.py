import pandas as pd
from matplotlib.ticker import MultipleLocator

from charting import fred, blp
from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag

def main():
    credit_df, credit_title = fred.get_series(series_id="TOTBKCR", observation_start="1976-01-01")
    credit_df = credit_df.resample("QS").last()

    gdp_df, gdp_title = fred.get_series(series_id="GDP", observation_start="1976-01-01")
    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start="19750101")

    credit_df = credit_df.pct_change(periods=4) * 100
    gdp_df = gdp_df.pct_change(periods=4) * 100

    final_df = credit_df - gdp_df

    title = "Bank Credit, GDP & CPI (YoY)"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="cpi_gdp.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(final_df.index, final_df['y'], label="Credit/GDP Diff")
    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title, transformer=Lag(offset=pd.DateOffset(months=24)))

    chart.add_horizontal_line()
    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()
