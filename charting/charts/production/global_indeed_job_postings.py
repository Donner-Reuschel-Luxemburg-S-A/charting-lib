import matplotlib.dates as mdates
from source_engine.indeed_source import IndeedSource

from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category


def main(**kwargs):
    indeed = IndeedSource()
    au, au_t = indeed.get_series(series_id="AU")
    ca, ca_t = indeed.get_series(series_id="CA")
    de, de_t = indeed.get_series(series_id="DE")
    fr, fr_t = indeed.get_series(series_id="FR")
    gb, gb_t = indeed.get_series(series_id="GB")
    us, us_t = indeed.get_series(series_id="US")

    title = "Indeed Job Postings"
    metadata = Metadata(title=title, region=Region.GLOBAL, category=Category.EMPLOYMENT)

    chart = Chart(title=title, filename="global_indeed_job_postings.jpeg", metadata=metadata)

    chart.configure_y_axis(label="Index")

    chart.configure_x_axis(major_formatter=mdates.DateFormatter("%b %y"))

    chart.add_series(au.index, au["indeed_job_postings_index_SA"].values, label=au_t)
    chart.add_series(ca.index, ca["indeed_job_postings_index_SA"].values, label=ca_t)
    chart.add_series(de.index, de["indeed_job_postings_index_SA"].values, label=de_t)
    chart.add_series(fr.index, fr["indeed_job_postings_index_SA"].values, label=fr_t)
    chart.add_series(gb.index, gb["indeed_job_postings_index_SA"].values, label=gb_t)
    chart.add_series(us.index, us["indeed_job_postings_index_SA"].values, label=us_t)

    chart.add_horizontal_line(y=100)
    chart.legend(ncol=3)

    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()
