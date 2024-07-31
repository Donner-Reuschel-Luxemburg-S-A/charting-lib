import datetime

from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    today = datetime.datetime.today().date()
    start = today - relativedelta(months=1)

    indices = ["S5ENRS Index", "S5CONS Index", "S5UTIL Index", "S5HLTH Index", "S5TELS Index", "S5MATR Index",
               "S5INDU Index", "S5COND Index", "S5FINL Index", "S5INFT Index", "S5RLST Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    names = ["Energy", "Consumer Staples", "Utilities", "Health Care", "Communication Services", "Materials",
             "Industrials", "Consumer Discretionary", "Financials", "IT", "Real Estate"]

    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"S&P 500 Sector Performance"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_sector_performance.jpeg")

    chart.configure_x_axis(label="PERCENTAGE POINTS")

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
