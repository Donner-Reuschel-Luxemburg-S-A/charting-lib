from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag


def main(**kwargs):
    blp = BloombergSource()

    cpi_df, cpi_title = blp.get_series(series_id="ECCPEMUY Index", observation_start="19990101")
    cpix_df, cpix_title = blp.get_series(series_id="CPEXEMUY Index", observation_start="19990101")
    m3_df, m3_title = blp.get_series(series_id="ECMAM3YY Index", observation_start="19990101")
    title = "EU Inflation and Money Supply (M3) YoY"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_m3_yoy.jpeg")
    chart.configure_y_axis(label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)
    chart.add_series(m3_df.index, m3_df['y'], label=m3_title, transformer=[Lag(DateOffset(months=0))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
