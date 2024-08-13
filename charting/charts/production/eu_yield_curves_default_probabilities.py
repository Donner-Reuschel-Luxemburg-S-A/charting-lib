import numpy as np
import pandas as pd
import xbbg.blp
from ratesvaluation.estimator import CurveEstimator

from charting.model.chart import Chart
from charting.model.curve_helper import build_curve, nss_curve, minimize_curve
from charting.model.metadata import Metadata, Region, Category
from ratesvaluation.provider import UnderlyingProvider


DEFAULT_START_TENOR = 0
DEFAULT_END_TENOR = 15


def main(**kwargs):
    def fix_bds_output(df, tenor='tenor', yld='mid_yield'):
        number = df[tenor].str[:-1].astype(float)
        div = df[tenor].str[-1].apply(lambda x: 12 if x == 'M' else 1)
        term = number / div
        df = pd.DataFrame(df[yld].values, index=term, columns=['y'])
        return df

    observation_start = kwargs.get('observation_start', DEFAULT_START_TENOR)
    observation_end = kwargs.get('observation_end', DEFAULT_END_TENOR)
    provider = UnderlyingProvider()
    estimators = {c: CurveEstimator(bonds=provider.get_bonds_for_country(c)) for c in ['DE', 'IT', 'RO', 'FR']}
    title = "EU Yield Curves"
    # metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title, filename="default_zcurve.jpeg")  # metadata=metadata,

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(label='TENOR')
    for c, est in estimators.items():
        tenor, z_curve = est.zero_curve()
        chart.add_series(chart_type='curve', x=tenor, y=z_curve, label=c, t_min=observation_start,
                         t_max=observation_end)
    chart.legend(2)
    chart.plot(upload_chart='observation_start' not in kwargs)
    df_curves = {}
    for c in ['IT', 'RO', 'FR']:
        df_curves[c] = estimators[c].default_curve(estimators['DE'])

    title = "EU Yield Curves"
    # metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title,  filename="default.jpeg")    #metadata=metadata,

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(label='TENOR')
    for c, (tenor, rates) in df_curves.items():
        cum_prob = 1-np.exp(-rates*np.array(tenor))
        chart.add_series(chart_type='curve', x=tenor[12:], y=(cum_prob[12:]-cum_prob[:-12])*100, label=c, t_min=observation_start,
                         t_max=observation_end)
    # chart.add_series(chart_type='curve', x=df2_smooth.index, y=df2_smooth['y'], label=t2, t_min=observation_start,
    #                  t_max=observation_end)
    # chart.add_series(chart_type='curve', x=df3.index, y=df3['y'], label=t3, t_min=observation_start,
    #                  t_max=observation_end)

    chart.legend(2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
