from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    blp = BloombergSource()

    indices = ["NDX Index", "INDU Index", "SPX Index", "RTY Index"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20120101") for idx in indices]

    names = [title for _, title in dfs]
    y = [df["y"].values for df, _ in dfs]

    title = f"U.S. Indices P/E Overview"

    metadata = Metadata(title=title, region=Region.US, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_indices_per_overview.jpeg")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
