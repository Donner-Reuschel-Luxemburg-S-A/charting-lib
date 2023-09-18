from source_engine.sdmx_source import Ecb

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
import matplotlib.dates as mdates


def main():
    source = Ecb()
    df1, t1 = source.get_data(flow_ref="EXR", key='D.CNY.EUR.SP00.A', parameters={'startPeriod': '2017-01-01'})

    title = "Chinese Yuan ¥"
    metadata = Metadata(title=title, region=[Region.EU, Region.DE, Region.CN], category=Category.FX)

    chart = Chart(title=title, metadata=metadata, filename="currency_eur_cny.png")

    chart.configure_y_axis(y_axis_index=0, label="CNY (¥)")

    major_locator = mdates.MonthLocator(interval=12)
    minor_locator = mdates.MonthLocator(interval=3)
    major_formatter = mdates.DateFormatter("%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator, major_locator=major_locator)

    chart.add_series(x=df1.index, y=df1['y'], label='ECB reference exchange rate, EUR/CNY')
    chart.add_last_value_badge(decimals=2)

    chart.legend()
    chart.plot()


if __name__ == '__main__':
    main()
