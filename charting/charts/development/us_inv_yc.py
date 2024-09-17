import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19600101"

    yc_df, yc_title = blp.get_series(series_id="USYC2Y10 Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "USA: Zinsstrukturkurve (2 Jahre vs. 10 Jahre) und Rezessionen"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_inv_yc", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(10), major_locator=MultipleLocator(50), label="Basispunkte")

    chart.add_series(yc_df.index, yc_df['y'], label=yc_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"])

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
