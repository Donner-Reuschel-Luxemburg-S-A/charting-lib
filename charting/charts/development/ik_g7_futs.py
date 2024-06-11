import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()

    start_time = "20240101"

    us10y_df, us10y_title = blp.get_series(series_id="USGG10YR Index", observation_start=start_time)

    de10y_df, de10y_title = blp.get_series(series_id="GDBR10 Index", observation_start=start_time)

    uk10y_df, uk10y_title = blp.get_series(series_id="G A Comdty", observation_start=start_time)

    au10y_df, au10y_title = blp.get_series(series_id="XMA Comdty", observation_start=start_time)

    ca10y_df, ca10y_title = blp.get_series(series_id="GCAN10YR Index", observation_start=start_time)

    jp10y_df, jp10y_title = blp.get_series(series_id="JBA Comdty", observation_start=start_time)

    title = "G7 Futures: Overview"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="ik_g7_rates10y.png", num_rows=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(.1), major_locator=MultipleLocator(.1), label="%")

    # chart.add_series(us2y_df.index, us2y_df['y'], label=us2y_title)
    chart.add_series(us10y_df.index, us10y_df['y'], label=us10y_title)

    # chart.add_series(de2y_df.index, de2y_df['y'], label=de2y_title)
    chart.add_series(ca10y_df.index, ca10y_df['y'], label=ca10y_title)

    # chart.add_series(uk2y_df.index, uk2y_df['y'], label=uk2y_title)
    chart.add_series(uk10y_df.index, uk10y_df['y'], label=uk10y_title)

    # chart.add_series(au2y_df.index, au2y_df['y'], label=au2y_title)
    chart.add_series(au10y_df.index, au10y_df['y'], label=au10y_title)

    # chart.add_series(ca2y_df.index, ca2y_df['y'], label=ca2y_title)
    chart.add_series(ca10y_df.index, ca10y_df['y'], label=ca10y_title)

    ##chart.add_series(jp2y_df.index, jp2y_df['y'], label=jp2y_title)
    # chart.add_series(jp10y_df.index, jp10y_df['y'], label=jp10y_title)

    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
