import os
from datetime import datetime, timedelta

import matplotlib.transforms
import numpy as np
import pandas as pd
import xbbg.blp
from matplotlib import pyplot as plt
from adjustText import adjust_text

from charting.model.bond_filter import at1_bonds
from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


DEFAULT_START_DATE = datetime.today()
DEFAULT_END_DATE = datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)
    x_col = 'YTM'
    y_col = 'YTC'
    df = at1_bonds()

    title = "Subordinate Bank AT1 Capital"
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)
    chart = Chart(title=title, filename="at1_ytc_ytm", metadata=metadata,
                  language=kwargs.get('language', 'en'))
    chart.add_series(df[x_col], df[y_col],
                     label=y_col.replace('_',' ').title() + ' / '+ x_col.replace('_',' ').title(),
                     chart_type='scatter')
    ##
    fig = chart.fig
    ax = chart.axis[0]
    trans_offset = matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=+.1, y=+.1, units='inches')
    texts = []

    for x, y, c in zip(df[x_col],df[y_col],  df.index):
        texts.append(plt.text(x, y, c, transform=trans_offset, fontdict={'size': 7}))

    ##
    x = np.arange(df[x_col].min()*.9,df[x_col].max()*1.1,.1)
    chart.add_series(x,x, label="Indifferent between Call / No Call")
    chart.configure_x_axis(label=x_col.replace('_',' ')+' in %')
    chart.configure_y_axis(label=y_col.replace('_',' ')+' in %')

    chart.legend(ncol=2)
    adjust_text(texts)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()

