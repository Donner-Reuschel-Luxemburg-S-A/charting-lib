import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()

    start_time = "20200201"

    rr_df, rr_title = blp.get_series(series_id="RRPQTOON Index", observation_start=start_time)
    tga_df, tga_title = blp.get_series(series_id="CERBTGAN Index", observation_start=start_time)
    fed_df, fed_title = blp.get_series(series_id="CERBTTAL Index", observation_start=start_time)

    spx_df, spx_title = blp.get_series(series_id="SPX Index", observation_start=start_time)

    df = fed_df
    df['y'] = df['y'] - rr_df['y'] - tga_df['y']

    title = "Net Liquidity vs. SPX"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="fed_spx.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1000), major_locator=MultipleLocator(1000), label="")

    chart.add_series(spx_df.index, spx_df['y'], label=spx_title)
    chart.add_series(df.index, df['y'], label="Net Liquidity", y_axis_index=1)

    chart.legend(ncol=1)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
