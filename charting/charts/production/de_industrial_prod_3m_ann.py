import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Category, Region
from charting.transformer.avg import Avg


def main(**kwargs):
    blp = BloombergSource()

    start_date = "20050101"

    de_ind_prod_df, de_ind_prod_title = blp.get_series(series_id="GRIPIMOM Index", observation_start=start_date)

    # Industrial Production
    title = "Germany Industrial Production: 3M Ann."
    metadata = Metadata(title=title, region=Region.DE, category=Category.ECONOMY)
    chart = Chart(title=title, filename="de_industrial_production_mom_3.jpeg", metadata=metadata)
    chart.configure_y_axis(label="%")

    chart.add_series(de_ind_prod_df.index, de_ind_prod_df['y'] * 12, label=de_ind_prod_title,
                     transformer=[Avg(offset=DateOffset(months=3))])

    chart.add_horizontal_line()
    chart.legend(ncol=2)
    return chart.plot(upload_chart='observation_start' not in kwargs)

if __name__ == '__main__':
    main()