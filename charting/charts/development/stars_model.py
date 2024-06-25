import time
from copy import deepcopy
from datetime import datetime
from source_engine.estat_statistics import EstatStatisticsSource
from source_engine.imf_source import ImfSource
from source_engine.sdmx_source import Ecb
from xbbg import blp
import pandas as pd
import matplotlib.transforms
import matplotlib.pyplot as plt
import numpy as np

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def output_results_to_excel(results, countries, file, **kwargs):
    mode = kwargs.get('mode', 'w')
    if mode == 'w':
        with pd.ExcelWriter(file, engine='openpyxl', date_format="YYYY-MM-DD",
                            datetime_format="YYYY-MM-DD", mode=mode) as writer:
            for key, value in results.items():
                value[countries].to_excel(writer, sheet_name=key,
                                          startcol=kwargs.get('startcol', 0),
                                          startrow=kwargs.get('startrow', 0))
    else:
        with pd.ExcelWriter(file, engine='openpyxl', date_format="YYYY-MM-DD",
                            datetime_format="YYYY-MM-DD", mode=mode,
                            if_sheet_exists='overlay') as writer:
            for key, value in results.items():
                value[countries].to_excel(writer, sheet_name=key,
                                          startcol=kwargs.get('startcol', 0),
                                          startrow=kwargs.get('startrow', 0))


def append_excel_results(file, results, countries):
    old_data = {}
    excel_file = pd.ExcelFile(file, engine='openpyxl')
    for sheet in excel_file.sheet_names:
        old_data[sheet] = excel_file.parse(sheet)
    col = max([df.shape[1] for df in old_data.values()])
    output_results_to_excel(results, countries, file, startcol=col + 2, mode='a')


def main():
    output_sheet = f'{datetime.today().strftime("%Y%m%d%H%M%S")} stars_output.xlsx'
    countries = ['DE', 'IT', 'FR', 'FI', 'NL', 'BE', 'AT', 'ES', 'PT', 'IE', 'SI', 'SK']
    period = 'A'
    imf_queries = {'primary_balance': ('FM', 'GGXONLB_G01_GDP_PT'), 'overall_balance': ('FM', 'GGXCNL_G01_GDP_PT'),
                   'international_reserves': ('IFS', 'RAFA_USD')}

    names = ['loan_to_deposit', 'housing_loans', 'unemployment_rate', 'government_debt', 'eco_sentiment',
             'industrial_sentiment', 'current_account', 'financial_account', 'labour_cost', 'savings_rate',
             'primary_balance', 'overall_balance', 'international_reserves']

    ecb_source = Ecb()
    estat_source = EstatStatisticsSource()

    estat_queries = {
        'unemployment_rate': 'tipsun30?format=JSON&sinceTimePeriod=2003-Q1&unit=PC_ACT&s_adj=SA&sex=T&age=Y15-74&lang=en',
        'government_debt': 'gov_10q_ggdebt?format=JSON&sinceTimePeriod=1994-Q4&unit=PC_GDP&na_item=GD&sector=S13&lang=en',
        'eco_sentiment': 'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ESI-I&s_adj=SA&lang=en',
        'industrial_sentiment': 'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ICI-BAL&s_adj=SA&lang=en',
        'current_account': 'bop_gdp6_q?format=JSON&freq=Q&sinceTimePeriod=2000-Q1&unit=PC_GDP&partner=WRL_REST&stk_flow=BAL&s_adj=NSA&bop_item=CA&lang=en',
        'financial_account': 'bop_gdp6_q?format=JSON&freq=Q&sinceTimePeriod=2000-Q1&unit=PC_GDP&partner=WRL_REST&stk_flow=N_LE&s_adj=NSA&bop_item=FA&lang=en',
        'labour_cost': 'ei_lmlc_q?format=JSON&sinceTimePeriod=2000-Q1&unit=I20&p_adj=NV&s_adj=SCA&nace_r2=B-N&indic=LM-LCI-TOT&lang=en',
        'savings_rate': 'tec00131?format=JSON&sinceTimePeriod=2011&unit=PC&na_item=SRG_S14_S15&sector=S14_S15&lang=en'
    }

    ecb_queries = {'loan_to_deposit': [
        ('CBD2', f'Q.{c}.W0.67._Z._Z.A.A.I3006._Z._Z._Z._Z._Z._Z.PC')
        for c in countries
    ], 'housing_loans': [
        ('CBD2', f'Q.{c}.W0.67._Z._Z.A.F.A1131._X.ALL.CA._Z.LE._T.EUR')
        for c in countries
    ]}

    ecb_result = {i: [] for i in ecb_queries.keys()}
    results = {}
    for index, queries in ecb_queries.items():
        for query in queries:
            ecb_result[index].append((*ecb_source.get_data(*query), query[1][2:4]))
        dfs = [t[0] for t in ecb_result[index]]
        dfs_c = [t[2] for t in ecb_result[index]]
        dfs = pd.concat(dfs, axis=1)
        dfs.columns = dfs_c
        results[index] = dfs
        print(index)

    estat_results = {}
    for key, query in estat_queries.items():
        out = estat_source.get_data(query)
        estat_results[key] = out
        results[key] = out.transpose()
        print(key)

    imf_result = {}
    i = 0
    for key, (dataset, s) in imf_queries.items():
        imf_result[key] = {}
        for c in countries:
            src = ImfSource()
            imf_result[key][c] = src.fetch_data(series=dataset, params=f'{period}.{c}.{s}')
            del src
            print(c)
            time.sleep(1)
        columns = list(imf_result[key].keys())
        dfs = [value[0]['OBS_VALUE'] for key, value in imf_result[key].items()]
        dfs = pd.concat(dfs, axis=1)
        dfs.columns = columns
        results[key] = dfs.astype(float)
        print(key)
        i += 1

    normalized_score = {}
    adj_value = {}
    for key, value in results.items():
        if 'sent' in key:
            normalized_score[key] = value[countries].ffill(axis=0).dropna(axis=1, how='all')
            adj_value[key] = value[countries].ffill(axis=0).dropna(axis=1, how='all')
            for c in countries:
                last_key = value[c].dropna().index[-1]
                if list(value[countries].index).index(last_key) != value[c].shape[0] - 1:
                    est = value['EU27_2020'].loc[last_key:].apply(lambda x: x - value['EU27_2020'].loc[last_key])
                    normalized_score[key].loc[last_key:, c] = normalized_score[key].loc[last_key:, c] + est
                    adj_value[key].loc[last_key:, c] = adj_value[key].loc[last_key:, c] + est

            normalized_score[key] = normalized_score[key]. \
                apply(lambda x: 2 * (x - x.min()) / (x.max() - x.min()) - 1, axis=1)
        else:
            normalized_score[key] = value[countries].ffill(axis=0).dropna(axis=1, how='all'). \
                apply(lambda x: 2 * (x - x.min()) / (x.max() - x.min()) - 1, axis=1)

    weights = {'initial_conditions': (0.4, {'government_debt': (.4, -1),
                                            'primary_balance': (.3, 1),
                                            'overall_balance': (.2, 1),
                                            'unemployment_rate': (.05, -1),
                                            'international_reserves': (.05, 1)}),
               'momentum': (.3, {'eco_sentiment': (.5, 1),
                                 'industrial_sentiment': (.5, 1)}),
               'competitivness': (.2, {'current_account': (.5, 1),
                                       'financial_account': (.3, 1),
                                       'labour_cost': (.2, -1)}),
               'leverage': (.1, {'housing_loans': (.4, -1),
                                 'loan_to_deposit': (.4, -1),
                                 'savings_rate': (.2, 1)})
               }
    data_table = pd.DataFrame(columns=countries, index=names, dtype=float)
    sector_table = pd.DataFrame(columns=countries, index=list(weights.keys()), dtype=float)
    total_score = pd.DataFrame(columns=countries, index=['Score'], dtype=float)
    for sector, data in weights.items():
        sector_weights = []
        for key, (weight, direction) in data[1].items():
            if key in ['primary_balance', 'overall_balance']:
                data_table.loc[key] = normalized_score[key][countries].loc[normalized_score[key][countries].index.year
                                                                           == datetime.now().year].squeeze()
            else:
                data_table.loc[key] = normalized_score[key][countries].iloc[-1, :] * direction
            sector_weights.append(weight)
        sector_table.loc[sector] = data_table.loc[list(data[1].keys())].multiply(sector_weights, axis=0).sum(axis=0)
    total_score.loc['Score'] = sector_table.multiply([data[0] for _, data in weights.items()], axis=0).sum(axis=0)
    total_df = pd.concat([total_score, sector_table, data_table], axis=0)
    total_df = total_df.loc[['Score', 'initial_conditions', 'government_debt', 'primary_balance',
                             'overall_balance', 'unemployment_rate', 'international_reserves',
                             'momentum', 'eco_sentiment', 'industrial_sentiment',
                             'competitivness', 'current_account', 'financial_account', 'labour_cost',
                             'leverage', 'housing_loans', 'loan_to_deposit', 'savings_rate']]

    tickers = {'DE': {5: 'GTDEM5Y Corp', 10: 'GTDEM10Y Corp'},
               'IT': {5: 'GTITL5Y Corp', 10: 'GTITL10Y Corp'},
               'FR': {5: 'GTFRF5Y Corp', 10: 'GTFRF10Y Corp'},
               'FI': {5: 'GTFIM5Y Corp', 10: 'GTFIM10Y Corp'},
               'NL': {5: 'GTNLG5Y Corp', 10: 'GTNLG10Y Corp'},
               'BE': {5: 'GTBEF5Y Corp', 10: 'GTBEF10Y Corp'},
               'AT': {5: 'GTATS5Y Corp', 10: 'GTATS10Y Corp'},
               'ES': {5: 'GTESP5Y Corp', 10: 'GTESP10Y Corp'},
               'PT': {5: 'GTPTE5Y Corp', 10: 'GTPTE10Y Corp'},
               'IE': {5: 'GTIEP5Y Corp', 10: 'GTIEP10Y Corp'},
               'SK': {5: 'GTSKK5Y Corp', 10: 'GTSKK10Y Corp'},
               'SI': {5: 'GTSIT5Y Corp', 10: 'GTSIT10Y Corp'}
               }
    ticker_result = deepcopy(tickers)
    spreads = deepcopy(tickers)
    for country, tenors in tickers.items():
        for tenor, ticker in tenors.items():
            ticker_result[country][tenor] = blp.bdp(ticker, flds='YLD_YTM_MID').iloc[0, 0]

    for country, tenors in tickers.items():
        for tenor, ticker in tenors.items():
            if country == 'DE':
                spreads[country][tenor] = 0
            else:
                spreads[country][tenor] = (ticker_result[country][tenor] - ticker_result['DE'][tenor]) * 100

    # Output results to xlsx
    output_results_to_excel({'OUTPUT_LONG': total_df}, countries, output_sheet, mode='w')
    output_results_to_excel({'OUTPUT_SHORT': sector_table}, countries, output_sheet, mode='a')
    output_results_to_excel({'OUTPUT_ALL': data_table}, countries, output_sheet, mode='a')
    output_results_to_excel(results, countries, output_sheet, mode='a')
    append_excel_results(output_sheet, normalized_score, countries)
    output_results_to_excel({'SPREADS': pd.DataFrame(spreads)}, countries, output_sheet, mode='a')

    # Charting
    title = '10-jähriger Spread vs. Fundamental Score'
    metadata = Metadata(title=title, region=Region.EU, category=[Category.RATES, Category.CREDIT, Category.FI])
    chart = Chart(filename='stars_model.jpeg', title=title, metadata=metadata)

    fig = chart.fig
    ax = chart.axis[0]
    trans_offset = matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=-.1, y=-.2, units='inches')
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.set_xlabel('Score')
    ax.set_ylabel('Spread vs. Bund', loc='top', labelpad=-50)
    ax.set_ylim(top=spreads['IT'][10] * 1.2)
    xs = total_score.loc['Score']
    ys = [spreads[country][10] for country in total_score.columns]

    chart.add_series(xs, ys, label='', chart_type='scatter')
    for x, y, c in zip(xs, ys, total_score.columns):
        if c == 'DE':
            plt.text(x, y, c,
                     transform=matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=-.1, y=.1, units='inches'))
        elif -0.1 < x < 0.1:
            plt.text(x, y, c,
                     transform=matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=-.3, y=-.2, units='inches'))
        else:
            plt.text(x, y, c, transform=trans_offset)
    m, b = np.polyfit(xs, ys, 1)
    xs_aux = np.linspace(xs.min() * 1.1, xs.max() * 1.1, 200)
    chart.add_series(xs_aux, m * xs_aux + b, label='')
    chart.plot()


if __name__ == '__main__':
    main()
