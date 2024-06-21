import datetime

from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2012, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indices = ["SX7P Index", "SXEP Index", "SXAP Index", "SXPP Index", "SX8P Index", "SX86P Index", "SXNP Index",
               "SX6P Index", "SXDP Index", "SXKP Index", "SXIP Index", "SX4P Index", "SXRP Index", "SX3P Index",
               "SXTP Index", "SXOP Index", "S600CPP index"]

    names = ["Banks", "Oil & Gas", "Autos & Parts", "Basic Resources", "Technology", "Real Estate", "Industrials",
             "Utilities", "Health Care", "Telecom", "Insurance", "Chemicals", "Retail", "Food & Beverage",
             "Travel", "Construction & Materials", "Consumer Products & Services"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    y = [df["y"].values for df, _ in dfs]

    title = f"Stoxx Euro 600 Sector P/E Overview"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxxp_sector_per_overview.png")

    chart.configure_x_axis(label="P/E")

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
