import datetime

from dateutil.relativedelta import relativedelta
from xbbg import blp
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category

DEFAULT_START_DATE = datetime.datetime.today() - relativedelta(years=5)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)


    indices = ["H27963EU Index", "H27964EU Index", "I10367EU Index", "I10370EU Index", "I02501EU Index", "H35142EU Index", "I31415EU Index"]
    names = ['Unternehmensanleihen A Rating', 'Unternehmensanleihen BBB Rating',
             'Banken A Rating', 'Banken BBB Rating',
             'Hochzins-Unternehmensanleihen', 'Hybrid-Unternehmensanleihen',
             'Regulatorisches AT1 Bankenkapital']
    dfs = [blp.bdh(idx, 'BX219', observation_start.strftime("%Y%m%d"),
                   observation_end.strftime("%Y%m%d"), Per='W') for idx in indices]


    y = [df.iloc[:, 0].values for df in dfs]

    title = f"Aufschläge verschiedener Unternehmensanleihe Typen"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.EQUITY)
    chart = Chart(title=title, metadata=metadata, filename="corp_credit_spreads", language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="BPS zu Swap")

    chart.add_series(names, y, label="", chart_type="boxplot",
                     t_min=min(df.index.min() for df in dfs), t_max=max(df.index.max() for df in dfs))

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
