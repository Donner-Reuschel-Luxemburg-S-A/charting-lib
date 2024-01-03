import datetime

import numpy as np
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from scipy import stats
from charting.model.chart import Chart


def main():
    blp = BloombergSource()

    indices = ["UKX Index", "DAX Index", "FTSEMIB Index", "PSI20 Index", "CAC Index", "AEX Index",
               "SMI Index", "IBEX Index"]

    dfs = [blp.get_series(series_id=idx, field="RR900", observation_start="20000101") for idx in indices]
    dfs = [df[np.abs(stats.zscore(df["y"])) < 2] for df, _ in dfs]

    y = [df["y"].values for df in dfs]

    names = ["FTSE 100 Index", "DAX Index", "FTSE MIB Index", "PSI 20 Index", "CAC 40 Index", "AEX-Index",
             "Swiss Market Index", "IBEX 35 Index"]

    title = f"European Indices P/E Overview"

    chart = Chart(title=title, filename="eu_indices_per_overview.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="P/E", minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(names, y, label="", chart_type="boxplot")

    chart.plot()


if __name__ == '__main__':
    main()
