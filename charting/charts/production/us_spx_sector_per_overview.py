from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()

    indices = ["S5RLST Index", "S5INDU Index", "S5COND Index", "S5FINL Index", "S5TELS Index", "S5MATR Index",
               "S5HLTH Index", "S5INFT Index", "S5CONS Index", "S5UTIL Index", "S5ENRS Index"]

    names = ["Real Estate", "Industrials", "Consumer Discretionary", "Financials", "Communication Services",
             "Materials", "Health Care", "IT", "Consumer Staples", "Utilities", "Energy"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20000101") for idx in indices]

    y = [df["y"].values for df, _ in dfs]

    title = f"S&P 500 Sector P/E Overview"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_sector_per_overview.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    chart.plot()


if __name__ == '__main__':
    main()
