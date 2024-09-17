import datetime

import pandas as pd
import xbbg.blp
from dateutil.relativedelta import relativedelta
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def get_bbg(query, field, start_date, end_date):
    try:
        return xbbg.blp.bdh(query, field, start_date=start_date, end_date=end_date).iloc[-1].values[0]
    except Exception as e:
        return None


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    indices = [
        "S600ENP Index",
        "SX4P Index",
        "SXPP Index",
        "SXOP Index",
        "SXNP Index",
        "SXMP Index",
        "SXAP Index",
        "SXRP Index",
        "S600CPP Index",
        "SXTP Index",
        "S600FOP Index",
        "S600PDP Index",
        "SXDP Index",
        "SXFP Index",
        "SX7P Index",
        "SXIP Index",
        "SX8P Index",
        "SXKP Index",
        "SX6P Index",
        "SX86P Index"
    ]

    dfs = [blp.get_series(series_id=idx, observation_start=observation_start.strftime("%Y%m%d"),
                          observation_end=observation_end.strftime("%Y%m%d")) for idx in indices]

    names = [
        "Energy",
        "Materials",
        "Materials",
        "Industrials",
        "Industrials",
        "Consumer Discretionary",
        "Consumer Discretionary",
        "Consumer Discretionary",
        "Consumer Discretionary",
        "Consumer Discretionary",
        "Consumer Staples",
        "Consumer Staples",
        "Health Care",
        "Financials",
        "Financials",
        "Financials",
        "Information Technology",
        "Communication Services",
        "Utilities",
        "Real Estate"
    ]

    yields = [((df['y'].iloc[-1] / df['y'].iloc[0]) - 1) * 100 for df, _ in dfs]
    market_caps = [get_bbg(index, field="CUR_MKT_CAP", start_date=(observation_end - relativedelta(weeks=1)).strftime('%Y%m%d'),
                            end_date=observation_end.strftime('%Y%m%d')) for index in indices]

    df = pd.DataFrame({
        'index': indices,
        'name': names,
        'yield': yields,
        'market_cap': market_caps
    })

    def weighted_yield(group):
        total_market_cap = group['market_cap'].sum()
        group['weight'] = group['market_cap'] / total_market_cap
        return (group['weight'] * group['yield']).sum()

    result = df.groupby('name').apply(weighted_yield)
    sorted_result = result.sort_values(ascending=True)

    title = f"Stoxx Euro 600 Sector Performance"

    metadata = Metadata(title=title, region=Region.EU, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="eu_sxxp_sector_performance", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="PERCENTAGE POINTS")

    chart.add_series(sorted_result.index, sorted_result, label="", chart_type="bar",
                     t_min=min(df.index.min() for df, _ in dfs), t_max=max(df.index.max() for df, _ in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
