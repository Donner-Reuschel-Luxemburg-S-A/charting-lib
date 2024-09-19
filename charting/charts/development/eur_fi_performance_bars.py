import datetime

from xbbg import blp

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
import pandas as pd
import locale
DEFAULT_START_DATE = datetime.date(2024, 1, 1)
DEFAULT_END_DATE = datetime.datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    # Get the current date
    today = datetime.datetime.today()

    # Get the last day of the previous year
    last_day_last_year = datetime.datetime(today.year - 1, 12, 31)

    # Use pandas to get the last business day of the month
    last_business_day = pd.Timestamp(last_day_last_year) - pd.offsets.BMonthEnd(1)
    end_day_ytd = pd.Timestamp(today) - pd.offsets.BDay(1)
    end_day_month = pd.Timestamp(today) - pd.offsets.MonthEnd(1)
    start_month = pd.Timestamp(today) - pd.offsets.MonthEnd(2)
    print("Last business day of last year:", last_business_day)

    assets = ["LBEATREU Index", "LEU1TREU Index",'BN8684431 Govt', 'ZJ6067798 Govt', 'I02003EU Index', 'LEGVTREU Index',
              'IS3C GY Equity', 'LECPTREU Index']
    ytd_dfs = [blp.bdp(idx, 'CUST_TRR_RETURN_HOLDING_PER',CUST_TRR_START_DT=last_day_last_year.strftime("%Y%m%d"),
                   CUST_TRR_END_DT=end_day_ytd.strftime("%Y%m%d")) for idx in assets]
    month_dfs = [blp.bdp(idx, 'CUST_TRR_RETURN_HOLDING_PER', CUST_TRR_START_DT=start_month.strftime("%Y%m%d"),
                       CUST_TRR_END_DT=end_day_month.strftime("%Y%m%d")) for idx in assets]
    names = ["Euro Agg", "Euro Agg 1-10", "DBRI 33", "DBR 33", 'Pfandbriefe', 'SSA',
             'Schwellenländer', 'Unternehmensanleihen']
    asset_yields_ytd = [df.iloc[0,0] for df in ytd_dfs]
    ytd_data = sorted(zip(names, asset_yields_ytd), key=lambda x: x[1])
    ytd_data = list(zip(*ytd_data))

    asset_yields_month = [df.iloc[0, 0] for df in month_dfs]
    month_data = sorted(zip(names, asset_yields_month), key=lambda x: x[1])
    month_data = list(zip(*month_data))
    title = f"Entwicklung Zinsmärkte"

    metadata = Metadata(title=title, region=Region.GLOBAL,
                        category=[Category.FI, Category.ALTERNATIVES])

    chart = Chart(title=title, metadata=metadata, filename="eur_fi_performance", num_rows=2, language=kwargs.get('language', 'en'))

    chart.configure_x_axis(label="PERCENTAGE POINTS")

    chart.add_series(month_data[0], month_data[1], label=f'Monat {end_day_month.strftime("%B")}', chart_type="bar",
                     t_min=start_month, t_max=end_day_month,
                     row_index=0)

    chart.add_series(ytd_data[0], ytd_data[1], label="YTD", chart_type="bar",
                     t_min=last_business_day, t_max=end_day_ytd,
                     row_index=1)
    chart.legend(2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
