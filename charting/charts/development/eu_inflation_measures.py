import matplotlib.dates as mdates
import numpy as np
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg
from charting.transformer.lag import Lag


def main(**kwargs):
    blp = BloombergSource()

    cpi_df, cpi_title = blp.get_series(series_id="ECCPEMUY Index", observation_start="19990101")
    cpix_df, cpix_title = blp.get_series(series_id="CPEXEMUY Index", observation_start="19990101")
    cpim_df, cpim_title = blp.get_series(series_id="ECCPEMUM Index", observation_start="19990101")
    cpixm_df, cpixm_title = blp.get_series(series_id="CPEXEMUM Index", observation_start="19990101")
    m3_df, m3_title = blp.get_series(series_id="ECMAM3YY Index", observation_start="19990101")

    title = "EU Inflation Measures YoY"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_measures_yoy", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "EU Inflation and Money Supply (M3) YoY"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_m3_yoy", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    chart.add_series(cpi_df.index, cpi_df['y'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['y'], label=cpix_title)
    chart.add_series(m3_df.index, m3_df['y'], label=m3_title, transformer=[Lag(DateOffset(months=0))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "EU Inflation Measures 6M Ann."
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_measures_mom_6", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=6))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=6))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "EU Inflation Measures 3M Ann."
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_measures_mom_3", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title,
                     transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

    title = "EU Inflation Measures 3M/3M Delta"
    metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_3m3m.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    cpim_df['y'] = cpim_df['y']-cpim_df['y'].shift(3)
    cpixm_df['y'] = cpixm_df['y'] - cpixm_df['y'].shift(3)

    chart.add_series(cpim_df.index, cpim_df['y'] * 12, label=cpim_title, transformer=[Avg(offset=DateOffset(months=3))])
    chart.add_series(cpixm_df.index, cpixm_df['y'] * 12, label=cpixm_title, transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    chart.plot()

    title = "EU Inflation Measures YoY: Change"
    metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, metadata=metadata, filename="eu_inflation_measures_yoy_delta", language=kwargs.get('language', 'en'))
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(2), label="%")

    cpi_df['z'] = np.diff(cpi_df['y'], prepend=0)
    cpix_df['z'] = np.diff(cpix_df['y'], prepend=0)

    chart.add_series(cpi_df.index, cpi_df['z'], label=cpi_title)
    chart.add_series(cpix_df.index, cpix_df['z'], label=cpix_title)

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
