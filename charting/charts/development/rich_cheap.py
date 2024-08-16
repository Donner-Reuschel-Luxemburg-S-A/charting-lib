from datetime import datetime

from ratesvaluation.estimator import CurveEstimator

from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata
from ratesvaluation.provider import UnderlyingProvider


DEFAULT_START_DATE = datetime.today()
DEFAULT_END_DATE = datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    title = "Teuer / Billig IT"
   # metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)
    chart = Chart(title=title, filename="rich_cheap",
                  language=kwargs.get('language', 'en'))

    provider = UnderlyingProvider()
    estimator = CurveEstimator(bonds=provider.get_bonds_for_country('IT'))
    t2, calculated_yields, original_yields = estimator.yields()
    t1, rates = estimator.par_curve()
    chart.add_series(t1, rates, label='Par Kurve')
    chart.add_series(t2, original_yields, linestyle='',label='Original Yields',  marker='x')
    chart.add_series([10], [rates[t1.index(10)]+30], marker='x',  label='IPT')
    chart.axis[0].text(10+0.1, rates[t1.index(10)]+30+5,'IPT')
    chart.configure_y_axis(y_axis_index=0, label="PERCENTAGE POINTS")

    chart.legend()

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()

