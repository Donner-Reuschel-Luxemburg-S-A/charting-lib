import datetime

from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main():
    blp = BloombergSource()

    today = datetime.datetime.today().date()
    start = today - relativedelta(months=1)

    indices = ["SXEGR Index", "SX3GR Index", "SXDGR Index", "SXTGR Index", "SXPGR Index", "SXIGR Index", "SXMGR Index",
               "SXQGR Index", "SXKGR Index", "SX4GR Index", "SX7GR Index", "SX6GR Index", "SXAGR Index", "SXNGR Index",
               "SXOGR Index", "SXFGR Index", "SXRGR Index", "SX8GR Index", "SX86GR Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=start.strftime("%Y%m%d")) for idx in indices]

    names = ["Oil & Gas", "Food & Beverage", "Health Care", "Travel", "Basic Resources", "Insurance", "Media",
             "Product & Households", "Telecom", "Chemicals", "Banks", "Utilities", "Autos & Parts", "Industrials",
             "Construction & Materials", "Financial Services", "Retail", "Technology", "Real Estate"]
    yields = [((df['y'].iloc[-1]/df['y'].iloc[0])-1)*100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"Stoxx Euro 600 Sector Performance - 1 Month ({start.strftime('%d.%m.%Y')} - {today.strftime('%d.%m.%Y')})"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxxp_sector_performance.png")

    chart.configure_y_axis(y_axis_index=0, label="")
    chart.configure_x_axis(label="Percentage Points", minor_locator=MultipleLocator(0.25), major_locator=MultipleLocator(1))

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    chart.plot()


if __name__ == '__main__':
    main()
