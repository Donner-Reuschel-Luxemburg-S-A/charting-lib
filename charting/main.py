from datetime import timedelta

from matplotlib.dates import DateFormatter
import pandas as pd
from charting.charts.time_series_chart import TimeSeriesChart
from charting.transformer.avg import Avg
from charting.transformer.invert import Invert
from charting.transformer.lag import Lag
from charting.transformer.lead import Lead

if __name__ == '__main__':
    # Example dataset
    data = {
        'Date': pd.date_range('2023-04-09', periods=10),
        'Series1': [10, 7, 3, 5, 9, 16, 14, 12, 25, 35],
        'Series2': [100, 120, 140, 150, 180, 200, 220, 250, 270, 300],
        'Series3': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        'Series4': [1040, 1030, 1020, 1010, 1000, 990, 980, 970, 960, 950]
    }

    df = pd.DataFrame(data)

    chart = TimeSeriesChart(title="Awesome Chart", num_y_axes=3)

    chart.configure_y_axis(axis_index=0, label="%", color='blue', y_lim=(-35, 35))
    chart.configure_y_axis(axis_index=1, label="Billion Dollar $", color='red', y_lim=(75, 325))
    chart.configure_y_axis(axis_index=2, label="Mio €", color='green')

    chart.configure_x_axis(formatter=DateFormatter("%d.%m.%Y"))

    chart.add_data(df['Date'], df['Series1'], label="Series 1", y_axis=0, color="blue",
                   transformer=Invert())
    chart.add_data(df['Date'], df['Series2'], label="Series 2", y_axis=1, color="red",
                   transformer=Avg(window=timedelta(days=2)))
    chart.add_data(df['Date'], df['Series3'], label="Series 3", y_axis=2, color="green",
                   transformer=Lead(window=timedelta(days=2)))
    chart.add_data(df['Date'], df['Series4'], label="Series 4", y_axis=2, color="green", linestyle='dashdot',
                   transformer=Lag(window=timedelta(days=4)))

    chart.legend(frameon=False, ncol=4)
    chart.plot(path="output/awesome-chart.png")
