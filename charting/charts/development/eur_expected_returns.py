import datetime

import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DataFrame
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from xbbg.blp import bdp
from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata
from charting.transformer.pct import Pct


def main():
    data = {'ticker': {'DE':
                           {4: 'GDBR4 Index',
                            5: 'GDBR5 Index',
                            9: 'GDBR9 Index',
                            10: 'GDBR10 Index'
                            },
                       'FR': {
                           4: 'GFRN4 Index',
                           5: 'GFRN5 Index',
                           9: 'GFRN9 Index',
                           10: 'GFRN10 Index'
                       },
                       'IT': {
                           4: 'GBTPGR4 Index',
                           5: 'GBTPGR5 Index',
                           9: 'GBTPGR9 Index',
                           10: 'GBTPGR10 Index'
                       },
                       'ES': {
                           4: 'GSPG4YR Index',
                           5: 'GSPG5YR Index',
                           9: 'GSPG9YR Index',
                           10: 'GSPG10YR Index'
                       },
                       'IG Corps A': {
                           4: 'IGEEVC04 Index',
                           5: 'IGEEVC05 Index',
                           9: 'IGEEVC09 Index',
                           10: 'IGEEVC10 Index'
                       },
                       'IG Corps BBB': {
                           4: 'BVCSBC04 Index',
                           5: 'BVCSBC05 Index',
                           9: 'BVCSBC09 Index',
                           10: 'BVCSBC10 Index'
                       },
                       'EUR Covered AAA': {
                           4: 'CVEETA04 Index',
                           5: 'CVEETA05 Index',
                           9: 'CVEETA09 Index',
                           10: 'CVEETA10 Index'
                       },
                       },
            'result': {}}
    for ticker, d in data.items():
        if ticker == 'ticker':
            for sector, mat in d.items():
                data['result'][sector] = {}
                for t, index in mat.items():
                    res = bdp(index, 'PX_LAST')
                    data['result'][sector][t] = res.iloc[0,0]
    title = "Expected Returns various Sectors"
    metadata = Metadata(title=title, region=Region.EU, category=[Category.RATES, Category.CREDIT, Category.FI])
    chart = Chart(title=title, metadata=metadata, filename="expected_returns10.png")

    chart.configure_y_axis(label="Percentage Points")

    date = datetime.datetime.now()
    x = list(data['result'].keys())
    y_roll_long = list([(sector[10] - sector[9])*9.5 for sector in data['result'].values()])
    y_yield_long = list([sector[10] for sector in data['result'].values()])


    y_roll_short = list([(sector[5] - sector[4]) * 4.5 for sector in data['result'].values()])
    y_yield_short = list([sector[5] for sector in data['result'].values()])
    category = ['5y', '10y']
    dict_ = {}
    for c in category:
        dict_[c] = {}
        for i, val in enumerate(x):
            if c == '5y':
                dict_[c][val] = {'Yield': y_yield_short[i], 'Roll': y_roll_short[i]}
            elif c == '10y':
                dict_[c][val] = {'Yield': y_yield_long[i], 'Roll': y_roll_long[i]}
    # for i, val in enumerate(x):
    #     dict_[val] = {category[0]: {y_yield_short[i] + y_roll_short[i]}, category[1]: y_yield_long[i] + y_roll_long[i]}
    counter = 0
    for key, value in dict_.items():
        chart.add_series([counter], {key: value}, label=key, chart_type='bar_grouped')
        counter += 1.5
    # title = "Erwartete Rendite 5-Jahres Sektor"
    # metadata = Metadata(title=title, region=Region.EU, category=[Category.RATES, Category.CREDIT, Category.FI])
    # chart5 = Chart(title=title, metadata=metadata, filename="expected_returns5.png")
    #
    # chart5.configure_y_axis(y_axis_index=0, label="Percentage Points", minor_locator=MultipleLocator(1),
    #                        y_lim=(0, 7))
    # chart5.add_series(x=x, y=y_yield_short, label="Kouponrendite", chart_type='bar', stacked=True, t_min=date,
    #                    t_max=date)
    # chart5.add_series(x=x, y=y_roll_short, label="Rolldown", chart_type='bar', stacked=True, t_min=date, t_max=date)
    #
    # chart10.plot()
    chart.legend(ncol=3)
    chart.plot()


if __name__ == '__main__':
    main()
