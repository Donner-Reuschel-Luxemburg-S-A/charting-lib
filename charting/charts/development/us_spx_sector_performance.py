import datetime

from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()

    today = datetime.datetime.today().date()
    start = today - relativedelta(months=1)

    indices = ["S5ENRS Index", "S5CONS Index", "S5UTIL Index", "S5HLTH Index", "S5TELS Index", "S5MATR Index",
               "S5INDU Index", "S5COND Index", "S5FINL Index", "S5INFT Index", "S5RLST Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=start.strftime("%Y%m%d")) for idx in indices]

    names = ["Energy", "Consumer Staples", "Utilities", "Health Care", "Communication Services", "Materials",
             "Industrials", "Consumer Discretionary", "Financials", "IT", "Real Estate"]

    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"S&P 500 Sector Performance - 1 Month ({start.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')})"

    chart = Chart(title=title, filename="us_spx_sector_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="%", minor_locator=MultipleLocator(0.25), major_locator=MultipleLocator(1))

    chart.add_series(data[0], data[1], label="", chart_type="bar")

    chart.plot()


if __name__ == '__main__':
    main()
