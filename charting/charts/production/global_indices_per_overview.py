import datetime

import matplotlib.dates as mdates
from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()

    indices = ["DAX Index", "SXXP Index", "SX5E Index", "SPX Index", "NDX Index", "INDU Index", "NKY Index",
               "MXEF Index"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20000101") for idx in indices]

    names = [title for _, title in dfs]
    y = [df["y"].values for df, _ in dfs]

    title = f"Global Indices P/E Overview"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="global_indices_per_overview.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    chart.plot()


if __name__ == '__main__':
    main()
