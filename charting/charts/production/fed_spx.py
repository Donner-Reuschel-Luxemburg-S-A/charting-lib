import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Region, Metadata, Category

DEFAULT_START_DATE = datetime.date(2020, 2, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    rr_df, rr_title = blp.get_series(series_id="RRPQTOON Index", observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    tga_df, tga_title = blp.get_series(series_id="CERBTGAN Index", observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))
    fed_df, fed_title = blp.get_series(series_id="CERBTTAL Index", observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))

    spx_df, spx_title = blp.get_series(series_id="SPX Index", observation_start=observation_start.strftime("%Y%m%d"),
                           observation_end=observation_end.strftime("%Y%m%d"))

    df = fed_df
    df['y'] = df['y'] - rr_df['y'] - tga_df['y']

    title = "Net Liquidity vs. SPX"
    metadata = Metadata(title=title, region=Region.US, category=Category.CB)

    chart = Chart(title=title, metadata=metadata, filename="fed_spx.png", num_rows=1, num_y_axis=2)
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))
    chart.configure_y_axis(label="Index")
    chart.configure_y_axis(label="Million USD $", y_axis_index=1)

    chart.add_series(spx_df.index, spx_df['y'], label=spx_title)
    chart.add_series(df.index, df['y'], label="Net Liquidity", y_axis_index=1)

    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
