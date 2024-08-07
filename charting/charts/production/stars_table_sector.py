import hashlib
from datetime import datetime
import pandas as pd
import numpy as np
import dataframe_image as dfi
import os
from charting import chart_base_path, base_path
from source_engine.chart_source import ChartSource, ChartModel

from charting import chart_base_path
from charting.model.chart import Chart
from charting.model.metadata import Region, Category


def main(**kwargs):
    n = datetime.now()
    destination = os.path.join(base_path, 'model_output')
    files = [f for f in os.listdir(destination) if os.path.isfile(os.path.join(destination, f))]
    files = list(filter(lambda x: 'stars_output' in x, files))
    files = list(filter(lambda x: x[:14].isdigit(), files))
    files = list(filter(lambda x: x[-4:] == "xlsx", files))
    date = [datetime.strptime(x[:14], "%Y%m%d%H%M%S") for x in files]
    min_date = [n - x for x in date]
    idx = min_date.index(min(min_date))
    file = files[idx]

    excel_file = pd.ExcelFile(os.path.join(destination, file), engine='openpyxl')
    sector_table = excel_file.parse('OUTPUT_SHORT', index_col=0)
    total_df = excel_file.parse('OUTPUT_LONG', index_col=0)
    data_table = excel_file.parse('OUTPUT_ALL', index_col=0)

    index = sector_table.index.to_list()
    index.append('Score')
    sl = pd.IndexSlice[index]
    filename = f'stars_sector_data'
    filename_date = f'{datetime.today().strftime("%d_%m_%Y")}_{filename}'
    filepath = os.path.join(chart_base_path, "production", filename_date)
    styled = total_df.style \
        .format(precision=2, decimal=',') \
        .apply(lambda x: ["font-weight: bold;" for v in x], axis=0, subset=(sl,)) \
        .apply_index(lambda x: np.where(x.isin(index), "font-weight: bold;", "font-weight: normal;"), axis=0) \
        .hide(data_table.index.to_list(), axis=0) \
        .map(lambda v: 'opacity: 40%;', subset=(pd.IndexSlice[sector_table.index.to_list(),])) \
        .format_index(lambda x: x.replace('_', ' ').upper() if isinstance(x, str) else x, axis=0) \
        .background_gradient(axis=0, cmap="bwr", vmin=-1, vmax=1)
    dfi.export(styled, filepath, table_conversion='playwright', dpi=200)
    db: ChartSource = ChartSource()
    chart_model = ChartModel(
        id=hashlib.sha1(filename.encode('utf-8')).hexdigest(),
        title="Stars Model Short",
        last_update=n,
        path=os.path.join("production", filename_date),
        module=Chart(filename)._caller(),
        start=n.date(),
        end=n.date(),
        region=','.join([Region.EU.value]),
        category=','.join([Category.FI.value, Category.RATES.value]),
        image=open(filepath, 'rb').read()
    )
    db.upload(chart=chart_model)


if __name__ == '__main__':
    main(language='en')
    main(language='de')
