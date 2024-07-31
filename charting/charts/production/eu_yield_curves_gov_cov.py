import pandas as pd
import xbbg.blp

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

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

    df1 = xbbg.blp.bds("BVIS0554 Index", "CURVE_TENOR_RATES")
    t1 = xbbg.blp.bdp("BVIS0554 Index", 'LONG_COMP_NAME')
    df1 = fix_bds_output(df1, yld='bid_yield')

    df2 = xbbg.blp.bds("BVIS0575 Index", "CURVE_TENOR_RATES")
    t2 = xbbg.blp.bdp("BVIS0575 Index", 'LONG_COMP_NAME')
    df2 = fix_bds_output(df2, yld='bid_yield')

    df3 = xbbg.blp.bds("BVSC0171 Index", "CURVE_TENOR_RATES")
    t3 = xbbg.blp.bdp("BVSC0171 Index", 'LONG_COMP_NAME')
    df3 = fix_bds_output(df3)

    title = "EU Yield Curves"
    metadata = Metadata(title=title, region=Region.EU, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="eu_yield_curves_gov_cov.jpeg")

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(label='TENOR')

    chart.add_series(chart_type='curve', x=df1.index, y=df1['y'], label=t1.iloc[0, 0], t_min=observation_start,
                     t_max=observation_end)
    chart.add_series(chart_type='curve', x=df2.index, y=df2['y'], label=t2.iloc[0, 0], t_min=observation_start,
                     t_max=observation_end)
    chart.add_series(chart_type='curve', x=df3.index, y=df3['y'], label=t3.iloc[0, 0], t_min=observation_start,
                     t_max=observation_end)

    chart.legend(2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()


