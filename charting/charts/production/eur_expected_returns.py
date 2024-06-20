from xbbg.blp import bdp
from charting.model.chart import Chart
from charting.model.metadata import Category, Region, Metadata


def main():
    data = {'ticker': {'DE Sov':
                           {4: 'GDBR4 Index',
                            5: 'GDBR5 Index',
                            9: 'GDBR9 Index',
                            10: 'GDBR10 Index'
                            },
                       'FR Sov': {
                           4: 'GFRN4 Index',
                           5: 'GFRN5 Index',
                           9: 'GFRN9 Index',
                           10: 'GFRN10 Index'
                       },
                       'IT Sov': {
                           4: 'GBTPGR4 Index',
                           5: 'GBTPGR5 Index',
                           9: 'GBTPGR9 Index',
                           10: 'GBTPGR10 Index'
                       },
                       'ES Sov': {
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
                       'Covered AAA': {
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
    title = "Expected Returns"
    metadata = Metadata(title=title, region=Region.EU, category=[Category.RATES, Category.CREDIT, Category.FI])
    chart = Chart(title=title, metadata=metadata, filename="expected_returns10.png")
    chart.configure_y_axis(label="Percentage Points", y_lim=(-1 ,7))

    x = list(data['result'].keys())
    y_roll_long = list([(sector[10] - sector[9])*9.5 for sector in data['result'].values()])
    y_yield_long = list([sector[10] for sector in data['result'].values()])

    y_roll_short = list([(sector[5] - sector[4]) * 4.5 for sector in data['result'].values()])
    y_yield_short = list([sector[5] for sector in data['result'].values()])
    category = ['5Y', '10Y']
    dict_ = {}
    for c in category:
        dict_[c] = {}
        for i, val in enumerate(x):
            if c == category[0]:
                dict_[c][val] = {'Yield': y_yield_short[i], 'Roll': y_roll_short[i]}
            elif c == category[1]:
                dict_[c][val] = {'Yield': y_yield_long[i], 'Roll': y_roll_long[i]}
    grouped_bar_width = .08
    bar_gap = .05
    counter = 0
    for idx, (key, value) in enumerate(dict_.items()):
        chart.add_series([counter], {key: value}, label=key, chart_type='bar_grouped',
                         grouped_bar_width=grouped_bar_width,
                         bar_gap=bar_gap)
        counter += (idx+1) * (len(value.keys())+2) * (bar_gap + grouped_bar_width)

    chart.legend(ncol=3)
    return chart.plot()


if __name__ == '__main__':
    main()
