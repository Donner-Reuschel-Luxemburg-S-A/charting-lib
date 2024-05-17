import datetime

from dateutil.relativedelta import relativedelta
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region


def main():
    blp = BloombergSource()
    end = (datetime.datetime.now().date()-datetime.timedelta(days=1))
    start = (datetime.datetime.now().date()-datetime.timedelta(days=365))
    stock_indices = ["SPX Index", "NDX Index", "RTY Index", "SXXP Index", "SX5E Index", "DAX Index", "NKY Index", "HSI Index"]
    stock_dfs = [blp.get_series(series_id=idx, observation_start=start.strftime("%Y%m%d"), observation_end=end.strftime("%Y%m%d")) for idx in stock_indices]
    stock_names = ["S&P 500", "NASDAQ 100", "Russell 2000", "Stoxx Europe 600", "Euro Stoxx 50", "DAX 40", "Nikkei 225", "Hang Seng"]
    stock_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in stock_dfs]
    stock_data = sorted(zip(stock_names, stock_yields), key=lambda x: x[1])
    stock_data = list(zip(*stock_data))

    cmdty_indices = ["XBTUSD Curncy", "XAG Curncy", "XAU Curncy", "CL1 Comdty", "EURUSD Curncy", "USDJPY Curncy", "EURCHF Curncy", "EURGBP Curncy"]
    cmdty_dfs = [blp.get_series(series_id=idx, observation_start=start.strftime("%Y%m%d"), observation_end=end.strftime("%Y%m%d")) for idx in
                 cmdty_indices]
    cmdty_names = ["Bitcoin USD", "Silver USD", "Gold USD", "Crude Oil WTI", "EUR/USD", "USD/JPY", "EUR/CHF", "EUR/GBP"]
    cmdty_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in cmdty_dfs]
    cmdty_data = sorted(zip(cmdty_names, cmdty_yields), key=lambda x: x[1])
    cmdty_data = list(zip(*cmdty_data))

    fi_indices = ["ER00 Index", "LEATTREU Index", "IBXXDECT Index", "IBOXXMJA Index", "JPEIHDEU Index"]
    fi_dfs = [blp.get_series(series_id=idx, observation_start=start.strftime("%Y%m%d"), observation_end=end.strftime("%Y%m%d")) for idx in
                 fi_indices]
    fi_names = ["Euro Corporate", "Euro-Aggregate: Treasury", "Covered Bonds", "EUR Liquid High Yield", "EMBI Global Core"]
    fi_yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in fi_dfs]
    fi_data = sorted(zip(fi_names, fi_yields), key=lambda x: x[1])
    fi_data = list(zip(*fi_data))

    title = f"Global Asset Class Performance - 1 Year ({start.isoformat()} - {end.isoformat()})"

    metadata = Metadata(title=title, region=Region.GLOBAL,
                        category=[Category.EQUITY, Category.FI, Category.ALTERNATIVES])

    chart = Chart(title=title, metadata=metadata, filename="global_asset_class_performance_last_year.png", num_rows=3)

    chart.configure_y_axis(y_axis_index=0, label="", row_index=0)
    chart.configure_y_axis(y_axis_index=0, label="", row_index=1)
    chart.configure_y_axis(y_axis_index=0, label="", row_index=2)

    chart.configure_x_axis(label="Percentage Points", minor_locator=MultipleLocator(5),
                           major_locator=MultipleLocator(20))

    chart.add_series(stock_data[0], stock_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in stock_dfs), t_max=max(df.index.max() for df, _ in stock_dfs),
                     row_index=0)

    chart.add_series(fi_data[0], fi_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in fi_dfs), t_max=max(df.index.max() for df, _ in fi_dfs),
                     row_index=1)

    chart.add_series(cmdty_data[0], cmdty_data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in cmdty_dfs), t_max=max(df.index.max() for df, _ in cmdty_dfs),
                     row_index=2)
    chart.plot()


if __name__ == '__main__':
    main()
