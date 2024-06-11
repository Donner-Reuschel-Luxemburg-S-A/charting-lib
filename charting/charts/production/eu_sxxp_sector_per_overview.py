from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()

    indices = ["SX7P Index", "SXEP Index", "SXAP Index", "SXPP Index", "SX8P Index", "SX86P Index", "SXNP Index",
               "SX6P Index", "SXDP Index", "SXKP Index", "SXIP Index", "SX4P Index", "SXRP Index", "SX3P Index",
               "SXTP Index", "SXOP Index", "S600CPP index"]

    names = ["Banks", "Oil & Gas", "Autos & Parts", "Basic Resources", "Technology", "Real Estate", "Industrials",
             "Utilities", "Health Care", "Telecom", "Insurance", "Chemicals", "Retail", "Food & Beverage",
             "Travel", "Construction & Materials", "Consumer Products & Services"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20120101") for idx in indices]

    y = [df["y"].values for df, _ in dfs]

    title = f"Stoxx Euro 600 Sector P/E Overview"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxxp_sector_per_overview.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
