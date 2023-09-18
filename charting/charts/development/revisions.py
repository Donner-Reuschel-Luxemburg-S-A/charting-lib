from matplotlib.ticker import FuncFormatter, MultipleLocator
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates


def millions(x, pos):
    return '%1.0f' % (x * 1e-3)


if __name__ == '__main__':
    fred = FredSource()
    chart = Chart(title="Revisions vs. Adjusted", num_y_axis=2,
                  filename="revisions-vs-adjusted.png")

    d0, t0 = fred.get_series(series_id='PAYEMS', observation_start="2020-01-01", observation_end="2023-06-30")
    d1, t1 = fred.get_series(series_id='PAYEMS', realtime_start="2020-01-01", realtime_end="2023-06-30",
                             observation_start="2020-01-01", observation_end="2023-06-30")
    diff = d1 - d0

    chart.configure_y_axis(y_axis_index=0, label="Millions of Persons", major_formatter=FuncFormatter(millions))
    chart.configure_y_axis(y_axis_index=1, label=u'Δ')

    major_locator = mdates.YearLocator(base=1)
    minor_locator = mdates.MonthLocator(interval=6)
    major_formatter = mdates.DateFormatter("%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_series(d0.index, d0["y"], label=t0)
    chart.add_series(d1.index, d1["y"], label=f'{t1} (Realtime)')
    chart.add_series(diff.index, diff["y"], y_axis_index=1, label='Revisions minus Adjusted')

    chart.legend()
    chart.plot()
