from matplotlib.ticker import MultipleLocator

from charting import fred, blp
from charting.model.chart import Chart
import matplotlib.dates as mdates

if __name__ == '__main__':
    credit_df, credit_title = fred.get_series(series_id="TOTBKCR", observation_start="1976-01-01")
    credit_df = credit_df.resample("QS").last()

    gdp_df, gdp_title = fred.get_series(series_id="GDP", observation_start="1976-01-01")
    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start="19750101")

    credit_df = credit_df.pct_change(periods=4) * 100
    gdp_df = gdp_df.pct_change(periods=4) * 100

    title = "Bank Credit, GDP & CPI (YoY)"
    chart = Chart(title=title, filename="cpi_gdp.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(credit_df.index, credit_df['y'], label=credit_title)
    chart.add_series(gdp_df.index, gdp_df['y'], label=gdp_title)
    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)

    chart.add_horizontal_line()
    chart.legend()
    chart.plot()
