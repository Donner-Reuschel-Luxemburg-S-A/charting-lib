import pandas as pd
from matplotlib.ticker import MultipleLocator
from source_engine.sdmx_source import Bbk

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
import matplotlib.dates as mdates

from charting.transformer.pct import Pct


def main():
    bbk = Bbk()
    d1, t1 = bbk.get_data(flow_ref="BBXP1", key="M.U2.N.HICP.000000.IND.I00", parameters={'startPeriod': '2006-01'})
    d1['y'] = d1['y'].astype(float)

    title = "Eurozone inflation"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_cpi_pmi.png")

    chart.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
                           major_locator=MultipleLocator(3))
    minor_locator = mdates.YearLocator(base=1)
    major_locator = mdates.YearLocator(base=3)
    major_formatter = mdates.DateFormatter("%b %y")
    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=d1.index, y=d1['y'], label="Eurozone Harmonized CPI", transformer=Pct(periods=12))
    chart.add_horizontal_line()

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()

