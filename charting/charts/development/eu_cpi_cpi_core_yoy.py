from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    cpi_df, cpi_title = blp.get_series(series_id="ECCPEMUY Index", observation_start="19990101")
    cpix_df, cpix_title = blp.get_series(series_id="CPEXEMUY Index", observation_start="19990101")

    title = "EU Inflation Measures YoY"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_cpi_cpi_core_yoy.png")
    chart.configure_y_axis(label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)

    chart.add_horizontal_line()
    chart.add_last_value_badge()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
