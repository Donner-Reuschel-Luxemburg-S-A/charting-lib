import os
from datetime import datetime, timedelta

import matplotlib.transforms
import numpy as np
import pandas as pd
import xbbg.blp
from matplotlib import pyplot as plt
from adjustText import adjust_text
from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


DEFAULT_START_DATE = datetime.today()
DEFAULT_END_DATE = datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)
    path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "Subordinate.xlsx")
    issuer = ['DB', 'SANTAN', 'UCGIM', 'ISPIM', 'RABOBK', 'CMZB', 'BKIR', 'SOGEN']
    df = pd.read_excel(path,
                       sheet_name="AT1", index_col="security_des().value", header=0, parse_dates=['issue_dt().value',
       'nxt_call_dt()', 'first_call_dt_issuance().value'])
    df.columns = ['ID', 'YTC', 'YTM',  'CPN', 'ISSUE_DT', 'NEXT_CALL_DT', 'FIRST_CALL_DT', 'RTG']
    df = df.dropna()
    sd_max = df['YTM'].std()*3+df['YTM'].mean()
    sd_min = df['YTM'].std() * -3 + df['YTM'].mean()
    df = df[(sd_min < df['YTM']) & (sd_max > df['YTM'])]
    sd_max = df['YTC'].std() * 3 + df['YTC'].mean()
    sd_min = df['YTC'].std() * -3 + df['YTC'].mean()
    df = df[(sd_min < df['YTC']) & (sd_max > df['YTC'])]
    df = df[df['ISSUE_DT']>pd.Timestamp(datetime.today().date()+timedelta(days=-4*365))]
    df = df[df.index.to_series().apply(lambda x: 'Float PERP' not in x)]
    df = df[df.index.to_series().apply(lambda x: x.split(' ')[0] in issuer)]
    title = "AT1"
   # metadata = Metadata(title=title, region=Region.EU, category=Category.INFLATION)
    chart = Chart(title=title, filename="at1",
                  language=kwargs.get('language', 'en'))
    chart.add_series(df['YTM'], df['YTC'], label='YTM/YTC', chart_type='scatter')
    ##
    fig = chart.fig
    ax = chart.axis[0]
    trans_offset = matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=+.1, y=+.1, units='inches')
    texts = []
    annotations = []
    for x, y, c in zip(df['YTM'], df['YTC'], df.index):
        texts.append(plt.text(x, y, c, transform=trans_offset, fontdict={'size': 7}))
        # annotations.append(plt.annotate('', xy=(x, y), xytext=(x+.1, y+.1), arrowprops=dict(arrowstyle='->', relpos=(.1,.1))))

    ##
    x = np.arange(df['YTM'].min()*.9,df['YTM'].max()*1.1,.1)
    chart.add_series(x,x, label="Undecided")
    chart.configure_x_axis(label='YTM')
    chart.configure_y_axis(label='YTC')

    chart.legend(ncol=2)
    adjust_text(texts)
    # for text, annotation in zip(texts, annotations):
    #     annotation.xytext = text.get_position()
    # chart.plot(upload_chart='observation_start' not in kwargs)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()

