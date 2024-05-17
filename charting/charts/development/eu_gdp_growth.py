from source_engine.estat_statistics import EstatStatisticsSource
import pandas as pd
from charting.model.chart import Chart
from charting.model.metadata import Metadata, Region, Category
import matplotlib.pyplot as plt
import numpy as np
def main():
    estat_source = EstatStatisticsSource()
    query = "namq_10_gdp?format=JSON&unit=CLV10_MEUR&s_adj=SCA&na_item=B1GQ&lang=en"

    data = estat_source.get_data(query)
    data = data.transpose()
    data_yoy = (data / data.shift(4) -1)*100
    title = "Manheim US Vehicle Inflation"
    metadata = Metadata(title=title, region=Region.US, category=Category.INFLATION)
    chart = Chart(title=title, metadata=metadata, filename="eu_gdp_growth.png", num_y_axis=1)
    countries = ['EA20', 'BE', 'DE', 'IE', 'ES', 'FR', 'IT', 'NL', 'AT', 'FI', 'SE', 'NO']
    margin = 0.5
    width = .25
    idxs = np.arange(-5,0,1)
    number_of_bars_per_x_label = len(idxs)
    number_of_x_labels = len(countries)
    x = np.linspace(0, number_of_bars_per_x_label * (number_of_x_labels-1) * (1 + margin) * width, num=number_of_x_labels)
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')
    for name, series in data_yoy[countries].iloc[idxs].iterrows():
        offset = width * multiplier
        rects = ax.bar(x+offset, series, width, label=name)
        # ax.bar_label(rects, padding=3)
        multiplier += 1

    # for name, series in data_yoy[countries].items():
    #     chart.add_series(idx[[-5,-1]], series.iloc[[-5,-1]].to_list(), name, chart_type='bar', stacked=True)
    ax.set_xticks(x + int(number_of_bars_per_x_label/2)*width, countries)
    ax.legend(loc='upper left', ncols=2)
    plt.savefig('eu_gdp_growth.png')
    # chart.legend()
    # chart.plot()

if __name__ == '__main__':
    main()