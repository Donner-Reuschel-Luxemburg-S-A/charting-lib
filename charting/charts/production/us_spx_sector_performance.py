import datetime

from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indices = ["S5BANKX Index", "S5AUCO Index", "S5SFTW Index", "S5CPGS Index", "S5RETL Index", "S5TRAN Index",
               "S5PHRM Index", "S5INSU Index", "S5TECH Index", "S5TELSX Index", "S5CODU Index", "S5MEDA Index",
               "S5HOUS Index", "S5HCES Index", "S5UTILX Index", "S5FDBT Index", "S5HOTR Index", "S5COMS Index",
               "S5DIVF Index", "S5FDSR Index", "S5FDSR Index"]
    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    names = ["Banks", "Autos & Parts", "Software & Services", "Capital Goods", "Consumer Discretionary", "Transportation",
             "Pharma, Biotech & Life Sciences", "Insurance", "Technology Hardware & Equipment", "Telecom",
             "Consumer Durables & Apparel", "Media & Entertainment", "Household & Personal Products", "Health Care Equipment & Services",
             "Utilities", "Food, Beverage & Tobacco", "Consumer Services", "Commercial & Professional Services",
             "Financial Services", "Consumer Staples", "Materials"]

    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]

    data = sorted(zip(names, yields), key=lambda x: x[1])
    data = list(zip(*data))

    title = f"S&P 500 Sector Performance"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="us_spx_sector_performance", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="PERCENTAGE POINTS")

    chart.add_series(data[0], data[1], label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
