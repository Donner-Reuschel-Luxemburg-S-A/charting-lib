import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart


def main():
    blp = BloombergSource()
    fred = FredSource()

    start_time = "19980101"

    cpi_df, cpi_title = blp.get_series(series_id="CPI YOY Index", observation_start=start_time)

    ism_manu_df, ism_manu_title = blp.get_series(series_id="NAPMPMI Index", observation_start=start_time)
    ism_manu_no_df, ism_manu_no_title = blp.get_series(series_id="NAPMNEWO Index", observation_start=start_time)
    ism_manu_inv_df, ism_manu_inv_title = blp.get_series(series_id="NAPMINV Index", observation_start=start_time)

    ism_manu_p_df, ism_manu_p_title = blp.get_series(series_id="NAPMPRIC Index", observation_start=start_time)

    ism_serv_df, ism_serv_title = blp.get_series(series_id="NAPMNMI Index", observation_start=start_time)
    ism_serv_p_df, ism_serv_p_title = blp.get_series(series_id="NAPMNPRC Index", observation_start=start_time)

    pmi_manu_df, pmi_manu_title = blp.get_series(series_id="MPMIUSMA Index", observation_start=start_time)
    pmi_serv_df, pmi_serv_title = blp.get_series(series_id="MPMIUSSA Index", observation_start=start_time)
    pmi_comp_df, pmi_comp_title = blp.get_series(series_id="MPMIUSCA Index", observation_start=start_time)

    pmi_chicago_df, pmi_chicago_title = blp.get_series(series_id="CHPMINDX Index", observation_start=start_time)

    lei_df, lei_title = blp.get_series(series_id="LEI YOY Index", observation_start=start_time)
    lei6m_df, lei6m_title = blp.get_series(series_id="LEI 6MAN Index", observation_start=start_time)

    confidence_df, confidence_title = blp.get_series(series_id="CONCCONF Index", observation_start=start_time)

    us_nber_df, us_nber_title = fred.get_series(series_id='JHDUSRGDPBR', observation_start=start_time)

    smallbusiness_opt_df, smallbusiness_opt_title = blp.get_series(series_id="SBOITOTL Index",
                                                                   observation_start=start_time)

    title = "US ISM Manufacturing & Services"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_ism.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(ism_manu_df.index, ism_manu_df['y'], label=ism_manu_title)
    # chart.add_series(ism_manu_no_df.index, ism_manu_no_df['y'], label="ISM Manufacturing New Orders")
    # chart.add_series(ism_manu_inv_df.index, ism_manu_inv_df['y'], label="ISM Manufacturing Inventories")
    chart.add_series(ism_serv_df.index, ism_serv_df['y'], label=ism_serv_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    # chart.add_series(ism_manu_no_df.index, (ism_manu_no_df['y'] - ism_manu_inv_df['y']).dropna(), label="ISM Manufacturing Book/Bill", row_index=1)

    chart.add_horizontal_line(y=50)
    chart.legend(ncol=2)
    chart.plot()

    title = "US PMIs"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_pmis.png", num_rows=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=1))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(pmi_manu_df.index, pmi_manu_df['y'], label=ism_manu_title)
    chart.add_series(pmi_serv_df.index, pmi_serv_df['y'], label=pmi_serv_title)
    chart.add_series(pmi_comp_df.index, pmi_comp_df['y'], label=pmi_comp_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=50)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Small Business Optimism"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_small_business_optimism.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5))

    chart.add_series(smallbusiness_opt_df.index, smallbusiness_opt_df['y'], label=smallbusiness_opt_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=100)
    chart.legend(ncol=2)
    chart.plot()

    title = "Chicago PMI"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_pmi_chicago.png", num_rows=1, num_y_axis=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="")

    chart.add_series(pmi_chicago_df.index, pmi_chicago_df['y'], label=pmi_chicago_title)
    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=50)
    chart.legend(ncol=2)
    chart.plot()

    title = "Conference Board Leading Indicator"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_leading_indicator.png", num_rows=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="")

    chart.add_series(lei_df.index, lei_df['y'], label=lei_title)
    chart.add_series(lei6m_df.index, lei6m_df['y'], label=lei6m_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=0)
    chart.legend(ncol=2)
    chart.plot()

    title = "US Consumer Confidence"
    # metadata = Metadata(title=title, region=Region.DE, category=Category.INFLATION)

    chart = Chart(title=title, filename="us_consumer_confidence.png", num_rows=1)
    chart.configure_x_axis(minor_locator=mdates.YearLocator(base=1), major_locator=mdates.YearLocator(base=5))
    chart.configure_y_axis(minor_locator=MultipleLocator(1), major_locator=MultipleLocator(5), label="")

    chart.add_series(confidence_df.index, confidence_df['y'], label=confidence_title)

    chart.add_vertical_line(x=us_nber_df.index, y=us_nber_df["y"], label=us_nber_title)

    chart.add_horizontal_line(y=100)
    chart.legend(ncol=2)
    chart.plot()


if __name__ == '__main__':
    main()
