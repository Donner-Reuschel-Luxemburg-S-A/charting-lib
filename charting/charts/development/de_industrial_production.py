import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource

from charting.model.chart import Chart


def main(**kwargs):
    blp = BloombergSource()

    start_date = "19500101"

    de_ind_prod_df, de_ind_prod_title = blp.get_series(series_id="GRIPIMOM Index", observation_start=start_date)

    ind = de_ind_prod_df
    ind['y'] = ind['y']

    ind['s'] = ind.groupby(ind['y'].gt(0).astype(int).diff().ne(0).cumsum()).cumcount().add(1) * ind['y'].gt(0).replace(
        {True: 1, False: -1})
    ind['s'] = ind['s'] * (-1)
    ind['s'] = ind['s'].clip(lower=0)

    title = "Germany: Consecutive Months of Decline in Industrial Production"
    # title = "Deutschland: Konsekutive Monate der Kontraktion in der Industrieproduktion"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="de_ind_prod_cons.png")
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(1), label="")

    chart.add_series(ind.index, ind['s'], label=de_ind_prod_title)

    chart.add_horizontal_line()
    chart.legend()
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
