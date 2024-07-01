import datetime

import matplotlib.dates as mdates
import pandas as pd
from source_engine.bloomberg_source import BloombergSource
from ratesvaluation.curves import SwapCurve
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from xbbg import blp as blp_
from scipy import optimize

DEFAULT_START_DATE = datetime.date(1999, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()
DAYS_PER_YEAR = 365

def helper_(r, swap_rate, schedule):
    sum_ = 1
    for key, value in schedule.items():
        if key != 'end':
            for v in value:
                sum_ *= 1 + key * v / DAYS_PER_YEAR
        else:
            for v in value:
                sum_ *= 1 + r * v / DAYS_PER_YEAR

    return sum_ - 1 - swap_rate * sum([sum(v) for v in schedule.values()]) / DAYS_PER_YEAR
def main(**kwargs):
    swap_curve = SwapCurve(ticker='YCSW0514 Index')

    ecb_meetings = blp_.bds('EURR002W Index','ECO_FUTURE_RELEASE_DATE_LIST')
    ecb_meetings = ecb_meetings.apply(lambda x: datetime.datetime.strptime(x[0][:10],'%Y/%m/%d'), axis=1).\
        reset_index(drop=True)

    ecb_meetings = ecb_meetings[ecb_meetings > datetime.datetime.today()]
    today = datetime.datetime.today().date()
    cb_rates = []
    for i, meeting in enumerate(ecb_meetings):
        if today == (meeting - datetime.timedelta(days=1)):
            current_rate = swap_curve.rate_at_time(ecb_meetings.iloc[0])
            cb_rates.append(current_rate)
        else:
            fix_swap_date = (meeting - datetime.timedelta(days=1)).to_pydatetime().date()
            days_per_rate = {}
            for j, m in enumerate(ecb_meetings.iloc[:i+1]):
                if j == 0:
                    start = today
                    range_ = pd.bdate_range(start, ecb_meetings.iloc[j]).diff().days.dropna().to_list()

                else:
                    start = ecb_meetings.iloc[j-1]
                    range_ = pd.bdate_range(start,
                                               ecb_meetings.iloc[j]).diff().days.dropna().to_list()
                if i == j:
                    days_per_rate['end'] = range_
                else:
                    days_per_rate[cb_rates[j]] = range_
            days_to_fix_swap_date = (fix_swap_date - today).days
            fix_swap_rate = swap_curve.rate_at_time(days_to_fix_swap_date/DAYS_PER_YEAR).rate
            initial_guess = swap_curve.rate_at_time(1/DAYS_PER_YEAR).rate if i == 0 else cb_rates[i-1]
            cb_rate = optimize.newton(helper_, initial_guess,
                    args=(fix_swap_rate, days_per_rate))
            cb_rates.append(cb_rate)

    rate_dates = [today]
    rate_dates.extend([x.to_pydatetime().date() for x in ecb_meetings[:-1]])
    title = "Central Banks - Key Interest Rates"
    chart = Chart(title=title, filename="global_key_interest_rates+pricing.jpeg")
    chart.add_series(x=rate_dates, y=cb_rates, label="ECB")
    chart.plot(upload_chart='observation_start' not in kwargs)




    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)

    blp = BloombergSource()

    d1, t1 = blp.get_series(series_id='UKBRBASE Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d2, t2 = blp.get_series(series_id='RBATCTR Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d3, t3 = blp.get_series(series_id='NOBRDEPA Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d4, t4 = blp.get_series(series_id='SWRRATEI Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d5, t5 = blp.get_series(series_id='FDTR Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d6, t6 = blp.get_series(series_id='EUORDEPO Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d7, t7 = blp.get_series(series_id='CABROVER Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    title = "Central Banks - Key Interest Rates"

    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.RATES)

    chart = Chart(title=title, metadata=metadata, filename="global_key_interest_rates.jpeg")

    chart.configure_y_axis(label="Percentage Points")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d1.index, y=d1["y"], label="United Kingdom")
    chart.add_series(x=d2.index, y=d2["y"], label="Australia")
    chart.add_series(x=d3.index, y=d3["y"], label="Norway")
    chart.add_series(x=d4.index, y=d4["y"], label="Sweden")
    chart.add_series(x=d5.index, y=d5["y"], label="United States")
    chart.add_series(x=d6.index, y=d6["y"], label="Eurozone")
    chart.add_series(x=d7.index, y=d7["y"], label="Canada", linestyle='--')
    chart.add_horizontal_line()

    chart.add_last_value_badge(decimals=2)
    chart.legend(ncol=3)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
