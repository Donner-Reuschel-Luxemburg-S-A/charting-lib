import pandas as pd
import xbbg.blp
from charting.model.chart import Chart
from charting.model.curve_helper import build_curve, nss_curve, minimize_curve
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
