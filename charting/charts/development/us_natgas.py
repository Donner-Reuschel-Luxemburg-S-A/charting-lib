import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19900101"

    ng_df, ng_title = blp.get_series(series_id="NG1 Comdty", observation_start=start_time)
    intm_df, intm_title = blp.get_series(series_id="BCOMIN Index", observation_start=start_time)
    xau_df, xau_title = blp.get_series(series_id="XAU Curncy", observation_start=start_time)
    cpi_df, cpi_title = blp.get_series(series_id="CPURNSA Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    title = "USA: Gaspreisentwicklung"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ng.jpeg", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="$/MMBtu")

    chart.add_series(ng_df.index, ng_df['y'], label=ng_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"])

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Preisentwicklung von Gold"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_gold.jpeg", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(50), major_locator=MultipleLocator(200), label="")

    chart.add_series(xau_df.index, xau_df['y'], label="Goldpreis in $")
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"])

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
