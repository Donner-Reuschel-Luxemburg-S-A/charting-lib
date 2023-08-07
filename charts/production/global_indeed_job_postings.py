import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
from charting import fred, indeed
from charting.transformer.lag import Lag
from charting.transformer.lead import Lead

if __name__ == '__main__':
    au, au_t = indeed.get_series(series_id="AU")
    ca, ca_t = indeed.get_series(series_id="CA")
    de, de_t = indeed.get_series(series_id="DE")
    fr, fr_t = indeed.get_series(series_id="FR")
    gb, gb_t = indeed.get_series(series_id="GB")
    jp, jp_t = indeed.get_series(series_id="JP")
    us, us_t = indeed.get_series(series_id="US")

    title = "Indeed Job Postings"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="global_indeed_job_postings.png", metadata=metadata)

    chart.configure_y_axis(y_axis_index=0, minor_locator=MultipleLocator(10), major_locator=MultipleLocator(20))

    chart.add_sup_y_label(label="%")

    major_locator = mdates.MonthLocator(interval=6)
    minor_locator = mdates.MonthLocator(interval=3)
    major_formatter = mdates.DateFormatter("%b-%Y")

    chart.configure_x_axis(major_formatter=major_formatter, minor_locator=minor_locator,
                           major_locator=major_locator)

    chart.add_series(au.index, au["indeed_job_postings_index_SA"].values, label=au_t)
    chart.add_series(ca.index, ca["indeed_job_postings_index_SA"].values, label=ca_t)
    chart.add_series(de.index, de["indeed_job_postings_index_SA"].values, label=de_t)
    chart.add_series(fr.index, fr["indeed_job_postings_index_SA"].values, label=fr_t)
    chart.add_series(gb.index, gb["indeed_job_postings_index_SA"].values, label=gb_t)
    chart.add_series(jp.index, jp["indeed_job_postings_index_SA"].values, label=jp_t)
    chart.add_series(us.index, us["indeed_job_postings_index_SA"].values, label=us_t, linestyle='--')

    chart.add_horizontal_line(y=100)

    chart.legend(ncol=4)
    chart.plot()
