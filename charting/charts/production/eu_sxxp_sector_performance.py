import datetime

from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indices = ["SXEGR Index", "SX3GR Index", "SXDGR Index", "SXTGR Index", "SXPGR Index", "SXIGR Index", "SXMGR Index",
               "SXQGR Index", "SXKGR Index", "SX4GR Index", "SX7GR Index", "SX6GR Index", "SXAGR Index", "SXNGR Index",
               "SXOGR Index", "SXFGR Index", "SXRGR Index", "SX8GR Index", "SX86GR Index", "S600CPP Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    names = ["Oil & Gas", "Food & Beverage", "Health Care", "Travel", "Basic Resources", "Insurance", "Media",
             "Product & Households", "Telecom", "Chemicals", "Banks", "Utilities", "Autos & Parts", "Industrials",
             "Construction & Materials", "Financial Services", "Retail", "Technology", "Real Estate", "Consumer Products"]
    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"Stoxx Euro 600 Sector Performance"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxxp_sector_performance", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="PERCENTAGE POINTS")

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
