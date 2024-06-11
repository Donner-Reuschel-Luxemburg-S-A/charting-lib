import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.transformer.avg import Avg


def main(**kwargs):
    blp = BloombergSource()

    cpi_df, cpi_title = blp.get_series(series_id="JNCPIYOY Index", observation_start="19600101")
    cpix_df, cpix_title = blp.get_series(series_id="JCPNEFFE Index", observation_start="19600101")
    tky_df, tky_title = blp.get_series(series_id="JNCPT Index", observation_start="19600101")
    cpim_df, cpim_title = blp.get_series(series_id="JNCPIMOM Index", observation_start="19600101")
    cpixm_df, cpixm_title = blp.get_series(series_id="JCPTFFMA Index", observation_start="19600101")
    tkym_df, tkym_title = blp.get_series(series_id="JNCPTMOM Index", observation_start="19600101")

    title = "Japan Inflation Measures YoY"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="jp_inflation_measures_yoy.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)
    chart.add_series(tky_df.index, tky_df['y'], label=tky_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Japan Inflation Measures 6M Ann."

    chart = Chart(title=title, filename="jp_inflation_measures_mom_6.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(tkym_df.index, tkym_df['y'] * 12, label=tkym_title, transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Japan Inflation Measures 3M Ann."

    chart = Chart(title=title, filename="jp_inflation_measures_mom_3.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(tkym_df.index, tkym_df['y'] * 12, label=tkym_title, transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "Japan Inflation Measures YoY: Change"

    chart = Chart(title=title, filename="jp_inflation_measures_yoy_delta.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="%")

    cpi_df['z'] = np.diff(cpi_df['y'], prepend=0)
    cpix_df['z'] = np.diff(cpix_df['y'], prepend=0)
    tky_df['z'] = np.diff(tky_df['y'], prepend=0)

    chart.add_series(cpi_df.index, cpi_df['z'] * 12, label=cpi_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpix_df.index, cpix_df['z'] * 12, label=cpix_title,
                     transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(tky_df.index, tky_df['z'] * 12, label=tky_title, transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
