from functools import partial

import numpy as np
import pandas as pd
import xbbg.blp
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from ratesvaluation.provider import _convert_to_int_or_zero, _update_cpn_freq, Bond
from ratesvaluation.estimator import CurveEstimator
import QuantLib as ql
from scipy.optimize import minimize

DEFAULT_START_TENOR = 0
DEFAULT_END_TENOR = 15

munhyp_covereds = [
    'BM136776 Corp',
    'BN560245 Corp',
    'ZS152894 Corp',
    'BP272138 Corp',
    'ZO264279 Corp',
    'ZF526438 Corp',
    'BY507121 Corp',
    'YW170134 Corp',
    'ZK915351 Corp',
    'BV780846 Corp',
    'ZK243088 Corp',
    'BT603105 Corp',
    'ZG138454 Corp',
    'EJ737221 Corp',
    'AT429189 Corp',
    'ZN216214 Corp',
    'AN420842 Corp',
    'AO791667 Corp',
    'ZI640732 Corp',
    'JK758200 Corp',
    'ZM520490 Corp',
    'EK792954 Corp'
]

flds = ['PX_MID', 'MTY_YEARS_TDY', 'CPN', 'CPN_FREQ', 'YLD_YTM_BID', 'YLD_YTM_ASK', 'YLD_YTM_MID',
        'DUR_ADJ_MID', 'REDEMP_VAL', 'INT_ACC', 'CNTRY_ISSUE_ISO', 'CURRENCY', 'MATURITY', 'ISSUE_DT', 'Ticker'
        ]


def nss_curve(x, theta):
    beta0, beta1, beta2, beta3, lambda1, lambda2 = x
    if lambda1 == 0 or lambda2 == 0:
        return np.inf
    term1 = beta0
    term2 = beta1 * ((1 - np.exp(-theta / lambda1)) / (theta / lambda1))
    term3 = beta2 * ((1 - np.exp(-theta / lambda1)) / (theta / lambda1) - np.exp(-theta / lambda1))
    term4 = beta3 * ((1 - np.exp(-theta / lambda2)) / (theta / lambda2) - np.exp(-theta / lambda2))
    return term1 + term2 + term3 + term4


def minimize_curve(observed_values):
    def _helper(x):
        sum_ = 0
        for t, yield_ in observed_values.items():
            sum_ += (yield_ - nss_curve(x, t)) ** 2
        return sum_

    result = minimize(_helper, np.array((.1, .1, .1, .1, 1, 1)), method="L-BFGS-B", options={'maxiter': 2500})
    return result


def build_curve():
    df = xbbg.blp.bdp(munhyp_covereds, flds)
    co_names = df.columns.to_list()
    co_names[1] = 'MTY_YEARS'
    co_names = [elem.upper() for elem in co_names]
    df.columns = co_names
    df.sort_values('MTY_YEARS', inplace=True)
    df = df[df['MTY_YEARS'] >= 0.25]

    df['CPN'] = df['CPN'] / 100
    df['MATURITY'] = df['MATURITY'].apply(lambda x: ql.Date(x.day, x.month, x.year))
    df['ISSUE_DT'] = df['ISSUE_DT'].apply(lambda x: ql.Date(x.day, x.month, x.year))
    df['CPN_FREQ'] = df['CPN_FREQ'].apply(_convert_to_int_or_zero)
    df['CPN_FREQ'] = df.apply(_update_cpn_freq, axis=1)
    df = df[df['MTY_YEARS'].between(0.08, 30)]

    bonds = []
    for _, row in df.iterrows():
        bond = Bond(row['CNTRY_ISSUE_ISO'], row['MATURITY'], row['MTY_YEARS'], row['CPN'], row['PX_MID'],
                    row['CPN_FREQ'], row['REDEMP_VAL'], row['CURRENCY'], row['YLD_YTM_MID'], row['ISSUE_DT'])
        bonds.append(bond)
    curve = CurveEstimator(bonds)
    return curve


def main(**kwargs):
    def fix_bds_output(df, tenor='tenor', yld='mid_yield'):
        number = df[tenor].str[:-1].astype(float)
        div = df[tenor].str[-1].apply(lambda x: 12 if x == 'M' else 1)
        term = number / div
        df = pd.DataFrame(df[yld].values, index=term, columns=['y'])
        return df

    observation_start = kwargs.get('observation_start', DEFAULT_START_TENOR)
    observation_end = kwargs.get('observation_end', DEFAULT_END_TENOR)

    t1 = 'Deutschland Staatsanleihen'
    df1 = xbbg.blp.bds("YCGT0016 Index", "CURVE_TENOR_RATES")
    df1 = fix_bds_output(df1, yld='bid_yield')
    result = minimize_curve(dict(zip(df1.index, df1['y'])))
    y = [nss_curve(result.x.tolist(), x) for x in df1.index]
    df1_smooth = pd.DataFrame(y, index=df1.index, columns=['y'])

    df2 = xbbg.blp.bds("YCGT0040 Index", "CURVE_TENOR_RATES")
    t2 = 'Italien Staatsanleihen'
    df2 = fix_bds_output(df2, yld='bid_yield')
    result = minimize_curve(dict(zip(df2.index, df2['y'])))
    y = [nss_curve(result.x.tolist(), x) for x in df2.index]
    df2_smooth = pd.DataFrame(y, index=df2.index, columns=['y'])

    # Covereds
    covered_curve = build_curve()
    par_curve = covered_curve.par_curve()
    df3 = pd.DataFrame({'y': [x / 100 for x in par_curve[1]]}, index=par_curve[0])
    t3 = 'Münchner Hypotheken Bank Pfandbriefe'

    title = "EU Yield Curves"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="eu_yield_curves_gov_cov.jpeg")

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(label='TENOR')

    chart.add_series(chart_type='curve', x=df1_smooth.index, y=df1_smooth['y'], label=t1, t_min=observation_start,
                     t_max=observation_end)
    chart.add_series(chart_type='curve', x=df2_smooth.index, y=df2_smooth['y'], label=t2, t_min=observation_start,
                     t_max=observation_end)
    chart.add_series(chart_type='curve', x=df3.index, y=df3['y'], label=t3, t_min=observation_start,
                     t_max=observation_end)

    chart.legend(2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
