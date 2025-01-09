import datetime

from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=10)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indices = ["NKY Index", "MXEF Index", "SXXP Index", "SX5E Index", "DAX Index", "NDX Index", "SPX Index"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    names = ["Nikkei 225", "Emerging Markets", "Stoxx Europe 600", "Euro Stoxx 50", "DAX 40",  "NASDAQ 100", "S&P 500"]

    y = [df["y"].values for df, _ in dfs]

    title = f"Global Indices P/E Overview"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="global_indices_per_overview", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="P/E")

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
