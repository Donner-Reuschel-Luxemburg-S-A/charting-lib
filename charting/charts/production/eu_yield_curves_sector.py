import numpy as np
import pandas as pd
import xbbg.blp

from charting.model.chart import Chart
from charting.model.curve_helper import minimize_curve, nss_curve
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_TENOR = 0
DEFAULT_END_TENOR = 15


euro_agg_corporate = [
    'LEC1TREU Index',
    'LEC3TREU Index',
    'LEC5TREU Index',
    'I02137EU Index',
    'I02138EU Index'
]

euro_agg_industrials = [
    'I10344EU Index',
    'I10345EU Index',
    'I10346EU Index',
    'I10347EU Index',
    'I10348EU Index'
]
euro_agg_utilities = [
    'I10349EU Index',
    'I10350EU Index',
    'I10351EU Index',
    'I10352EU Index',
    'I10353EU Index'
]
euro_agg_financials = [
    'I10354EU Index',
    'I10355EU Index',
    'I10356EU Index',
    'I10357EU Index',
    'I10358EU Index'
]

sectors = {
    'euro_agg_corp': euro_agg_corporate,
    'euro_agg_industrials': euro_agg_industrials,
    'euro_agg_utilities': euro_agg_utilities,
    'euro_agg_financials': euro_agg_financials
}


def main(**kwargs):

    observation_start = kwargs.get('observation_start', DEFAULT_START_TENOR)
    observation_end = kwargs.get('observation_end', DEFAULT_END_TENOR)

    title = "EU Corporate Spreads by Sector"
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)
    chart = Chart(title=title, metadata=metadata, filename="eu_corporate_curves_sector.jpeg")
    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(label='TENOR')

    data = {}
    curves = {}

    x = np.linspace(1,15,29).tolist()
    for key, value in sectors.items():
        data[key] = xbbg.blp.bdp(value, ['INDEX_TIME_TO_MATURITY', 'INDEX_YIELD_TO_MATURITY'])
        data[key] = dict(zip(data[key]['index_time_to_maturity'].to_list(), data[key]['index_yield_to_maturity'].to_list()))
        curves[key] = minimize_curve(data[key])
        y = [nss_curve(curves[key].x.tolist(), x_) for x_ in x]
        name = key.title().replace('_',' ')
        chart.add_series(chart_type='curve', x=x, y=y, label=name, t_min=observation_start,
                         t_max=observation_end)

    chart.legend(2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
