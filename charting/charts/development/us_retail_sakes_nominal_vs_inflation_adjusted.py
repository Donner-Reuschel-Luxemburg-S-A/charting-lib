from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.transformer.pct import Pct

if __name__ == '__main__':
    fred = FredSource()
    chart = Chart(title="US Retail Sales - Nominal vs. Inflation Adjusted", num_rows=2, num_y_axis=1,
                  filename="us_retail_sakes_nominal_vs_inflation_adjusted.png")

    d0, t0 = fred.get_series(series_id='MRTSSM44000USS', observation_start="1992-01-01")

    chart.configure_y_axis(row_index=0, y_axis_index=0)
    chart.configure_y_axis(row_index=1, y_axis_index=0)
    chart.add_sup_y_label(label="%")

    major_locator = mdates.YearLocator(base=5)
    minor_locator = mdates.YearLocator(base=1)
    major_formatter = mdates.AutoDateFormatter(major_locator)

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_series(d0.index, d0["y"], row_index=0, label=t0,
                     transformer=Pct(periods=12))

    chart.add_last_value_badge()
    chart.legend(ncol=2)
    chart.plot()
