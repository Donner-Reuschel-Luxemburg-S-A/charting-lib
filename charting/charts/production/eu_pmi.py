import matplotlib.dates as mdates
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    df10, t10 = blp.get_series(series_id='MPMIEZCA Index', observation_start=start_date)
    df11, t11 = blp.get_series(series_id='MPMIFRCA Index', observation_start=start_date)
    df12, t12 = blp.get_series(series_id='MPMIITCA Index', observation_start=start_date)
    df13, t13 = blp.get_series(series_id='MPMIDECA Index', observation_start=start_date)

    title = "Composite PMIs: Eurozone"
    metadata = Metadata(title=title, region=Region.DE, category=Category.SURVEY)

    chart = Chart(title=title, metadata=metadata, filename="eu_pmi.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="Index")

    major_formatter = mdates.DateFormatter("%b %y")

    chart.configure_x_axis(major_formatter=major_formatter)

    chart.add_series(x=df10.index, y=df10['y'], label=t10)
    chart.add_series(x=df11.index, y=df11['y'], label=t11)
    chart.add_series(x=df12.index, y=df12['y'], label=t12)
    chart.add_series(x=df13.index, y=df13['y'], label=t13)

    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()