import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from source_engine.bloomberg_source import BloombergSource
from ratesvaluation.curves import SwapCurve
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from xbbg import blp as blp_
from scipy import optimize
import charting.model.style as style

DEFAULT_START_DATE = datetime.date(2018, 1, 1)
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
    mat = sum([sum(v) for v in schedule.values()])
    swap_rate_comp = 1 + swap_rate * mat / DAYS_PER_YEAR if mat / DAYS_PER_YEAR <= 1 else (1+swap_rate)**(mat/DAYS_PER_YEAR)
    return sum_ - swap_rate_comp


def main(**kwargs):
    today = datetime.datetime.today().date()

    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)
    title = "Central Banks - Key Interest Rates"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.RATES)
    chart = Chart(title=title, metadata=metadata, filename="global_key_interest_rates+pricing.jpeg")

    blp = BloombergSource()
    d5, t5 = blp.get_series(series_id='FDTR Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d6, t6 = blp.get_series(series_id='EUORDEPO Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d7, t7 = blp.get_series(series_id='UKBRBASE Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))
    d8, t8 = blp.get_series(series_id='BOJDTR Index', observation_start=observation_start.strftime("%Y%m%d"),
                            observation_end=observation_end.strftime("%Y%m%d"))

    chart.configure_y_axis(label="PERCENTAGE POINTS")
    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(x=d5.index, y=d5["y"], label=t5, color=style.get_color(2))
    chart.add_series(x=d6.index, y=d6["y"], label=t6, color=style.get_color(1))
    chart.add_series(x=d7.index, y=d7["y"], label=t7, color=style.get_color(3))
    chart.add_series(x=d8.index, y=d8["y"], label=t8, color=style.get_color(4))
    chart.add_horizontal_line()
    chart.legend(ncol=2)


    curves = {'ECB': {},
              'FED': {},
              'BOE': {},
              'BOJ': {}
              }

    # EUR
    eur_curve = SwapCurve(ticker='YCSW0514 Index')
    ecb_meetings = blp_.bds('EURR002W Index', 'ECO_FUTURE_RELEASE_DATE_LIST')
    ecb_meetings = ecb_meetings.apply(lambda x: datetime.datetime.strptime(x[0][:10], '%Y/%m/%d'), axis=1). \
        reset_index(drop=True)

    ecb_meetings = ecb_meetings[ecb_meetings > datetime.datetime.today()]
    while ecb_meetings.iloc[-1].to_pydatetime().date() < today + datetime.timedelta(days=365*3):
        ecb_meetings = pd.concat([ecb_meetings, pd.Series([ecb_meetings.iloc[-1] + datetime.timedelta(days=45)],
                                                          index=[1+ecb_meetings.index[-1]])])
    curves['ECB'] = {'CURVE': eur_curve, 'MEETING_DATES': ecb_meetings,'HISTORY': d6}

    # USD
    usd_curve = SwapCurve(ticker='YCSW0490 Index')
    usd_on = blp_.bdp('SOFRRATE Index', 'PX_LAST')
    fdates = [1/365]
    fdates.extend(usd_curve.dates[0])
    usd_curve.dates = fdates
    usd_rates = [usd_on.iloc[0,0]/100]
    usd_rates.extend((usd_curve._data['mid_yield'] / 100).tolist())
    usd_curve._rates = []
    usd_curve.rates = usd_rates
    fed_meetings = blp_.bds('FDTR Index', 'ECO_FUTURE_RELEASE_DATE_LIST')
    fed_meetings = fed_meetings.apply(lambda x: datetime.datetime.strptime(x[0][:10], '%Y/%m/%d'), axis=1). \
        reset_index(drop=True)
    fed_meetings = fed_meetings[fed_meetings > datetime.datetime.today()]
    while fed_meetings.iloc[-1].to_pydatetime().date() < today + datetime.timedelta(days=365*3):
        fed_meetings = pd.concat([fed_meetings, pd.Series([fed_meetings.iloc[-1] + datetime.timedelta(days=45)], index=[1+fed_meetings.index[-1]])])
    curves['FED'] = {'CURVE': usd_curve, 'MEETING_DATES': fed_meetings,'HISTORY': d5}

    # GBP
    gbp_curve = SwapCurve(ticker='YCSW0141 Index')
    gbp_on = blp_.bdp('SONIO/N Index', 'PX_LAST')
    fdates = [1 / 365]
    fdates.extend(gbp_curve.dates[0])
    gbp_curve.dates = fdates
    gbp_rates = [gbp_on.iloc[0, 0] / 100]
    gbp_rates.extend((gbp_curve._data['mid_yield'] / 100).tolist())
    gbp_curve._rates = []
    gbp_curve.rates = gbp_rates
    boe_meetings = blp_.bds('UKBRBASE Index', 'ECO_FUTURE_RELEASE_DATE_LIST')
    boe_meetings = boe_meetings.apply(lambda x: datetime.datetime.strptime(x[0][:10], '%Y/%m/%d'), axis=1). \
        reset_index(drop=True)
    boe_meetings = boe_meetings[boe_meetings > datetime.datetime.today()]
    while boe_meetings.iloc[-1].to_pydatetime().date() < today + datetime.timedelta(days=365 * 3):
        boe_meetings = pd.concat([boe_meetings, pd.Series([boe_meetings.iloc[-1] + datetime.timedelta(days=45)],
                                                          index=[1 + boe_meetings.index[-1]])])
    curves['BOE'] = {'CURVE': gbp_curve, 'MEETING_DATES': boe_meetings, 'HISTORY': d7}

    # JPY
    jpy_curve = SwapCurve(ticker='YCSW0195 Index')
    jpy_on = blp_.bdp('MUTKCALM Index', 'PX_LAST')
    fdates = [1 / 365]
    fdates.extend(jpy_curve.dates[0])
    jpy_curve.dates = fdates
    jpy_rates = [jpy_on.iloc[0, 0] / 100]
    jpy_rates.extend((jpy_curve._data['mid_yield'] / 100).tolist())
    jpy_curve._rates = []
    jpy_curve.rates = jpy_rates
    boj_meetings = blp_.bds('UKBRBASE Index', 'ECO_FUTURE_RELEASE_DATE_LIST')
    boj_meetings = boj_meetings.apply(lambda x: datetime.datetime.strptime(x[0][:10], '%Y/%m/%d'), axis=1). \
        reset_index(drop=True)
    boj_meetings = boj_meetings[boj_meetings > datetime.datetime.today()]
    while boj_meetings.iloc[-1].to_pydatetime().date() < today + datetime.timedelta(days=365 * 3):
        boj_meetings = pd.concat([boj_meetings, pd.Series([boj_meetings.iloc[-1] + datetime.timedelta(days=45)],
                                                          index=[1 + boj_meetings.index[-1]])])
    curves['BOJ'] = {'CURVE': jpy_curve, 'MEETING_DATES': boj_meetings, 'HISTORY': d8}
    for cb, data in curves.items():
        cb_rates = []
        swap_curve = data['CURVE']
        meetings = data['MEETING_DATES']
        cb_rates.append(swap_curve.rate_at_time(1/365).rate)
        for i, meeting in enumerate(meetings):
            if i == 0:
                continue
            if today == (meeting - datetime.timedelta(days=1)):
                current_rate = swap_curve.rate_at_time(meetings.iloc[0])
                cb_rates.append(current_rate)
            else:
                fix_swap_date = (meeting - datetime.timedelta(days=1)).to_pydatetime().date()
                days_per_rate = {}
                for j, m in enumerate(meetings.iloc[:i+1]):
                    if j == 0:
                        start = today
                        range_ = pd.bdate_range(start, meetings.iloc[j]).diff().days.dropna().to_list()

                    else:
                        start = meetings.iloc[j-1]
                        range_ = pd.bdate_range(start, meetings.iloc[j]).diff().days.dropna().to_list()
                    if i == j:
                        days_per_rate['end'] = range_
                    else:
                        days_per_rate[cb_rates[j]] = range_
                days_to_fix_swap_date = (fix_swap_date - today).days - 2
                fix_swap_rate = swap_curve.rate_at_time(days_to_fix_swap_date/DAYS_PER_YEAR)
                if days_to_fix_swap_date / DAYS_PER_YEAR >=1:
                    fix_swap_rate.compounding_frequency = 1
                fix_swap_rate = fix_swap_rate.rate
                initial_guess = cb_rates[i-1]
                cb_rate = optimize.newton(helper_, initial_guess,
                        args=(fix_swap_rate, days_per_rate))
                cb_rates.append(cb_rate)

        rate_dates = [today]
        rate_dates.extend([x.to_pydatetime().date() for x in meetings[:-1]])
        priced = pd.DataFrame({'Rates': cb_rates}, index=pd.DatetimeIndex(rate_dates))
        curves[cb]['PRICED'] = priced
        priced = priced.resample('D').ffill()
        curves[cb]['PRICED_FILLED'] = priced

    counter = 1
    for cb, data in curves.items():
        correction = (curves[cb]['HISTORY'].iloc[-1, 0]-data['PRICED_FILLED']['Rates'].iloc[0]*100)
        chart.add_series(x=data['PRICED_FILLED'].index, y=data['PRICED_FILLED']['Rates']*100+correction,
                         label=f'{cb} OIS Implied', color=style.get_color(counter), alpha=.5)
        counter += 1
    plt.text(today+datetime.timedelta(days=(1.2*365)), 5.2, 'OIS Implied Rates',fontsize=8)

    chart.add_last_value_badge(decimals=2)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
