import os
from datetime import datetime, timedelta
from charting.model.style import colors
import matplotlib.transforms
import numpy as np
import pandas as pd
import xbbg.blp
from matplotlib import pyplot as plt
from adjustText import adjust_text

from charting.model.bond_filter import at1_bonds, non_fin_bonds
from charting.model.chart import Chart
from charting.model.metadata import Region, Category, Metadata


DEFAULT_START_DATE = datetime.today()
DEFAULT_END_DATE = datetime.today()


def main(**kwargs):
    observation_start = kwargs.get('observation_start', DEFAULT_START_DATE)
    observation_end = kwargs.get('observation_end', DEFAULT_END_DATE)
    x_col = 'NEXT_CALL_DT'
    y_col = 'YTC'
    df = non_fin_bonds()

    title = "Non-Financial Subordinate Capital"
    metadata = Metadata(title=title, region=Region.EU, category=Category.CREDIT)
    chart = Chart(title=title, filename="sub_term_structure", metadata=metadata,
                  language=kwargs.get('language', 'en'))
    fig = chart.fig
    ax = chart.axis[0]
    trans_offset = matplotlib.transforms.offset_copy(ax.transData, fig=fig, x=+.1, y=+.1, units='inches')
    texts = []
    counter = 0
    for ticker, df_ in df.groupby('TICKER'):
        col_ = (colors[counter], 1)
        x = np.linspace(min(df_['YEARS_TO_CALL'])*0.85, max(df_['YEARS_TO_CALL'])*1.05,50)
        y = np.polyfit(df_['YEARS_TO_CALL'], df_[y_col],3)
        y_fn = np.poly1d(y)
        chart.add_series(df_[x_col],df_[y_col] ,
                         label=ticker,
                         chart_type='scatter',
                         color=col_)
        chart.add_series([pd.Timestamp(datetime.today().date() + timedelta(days=int(365*x_years))) for x_years in x], y_fn(x),
                         label=ticker,
                         chart_type='line',
                         color=col_)
        for x, y, c in zip(df_[x_col],df_[y_col],  df_.index):
            texts.append(plt.text(x, y, c, transform=trans_offset, fontdict={'size': 7}))
        counter += 1


    chart.configure_x_axis(label='Next Call Date')
    chart.configure_y_axis(label='YTC in %')

    # chart.legend(ncol=2)
    adjust_text(texts)
    return chart.plot(upload_chart='observation_start' not in kwargs)


if __name__ == '__main__':
    main()

