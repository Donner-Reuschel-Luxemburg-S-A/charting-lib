from datetime import datetime
import pandas as pd
import numpy as np
import dataframe_image as dfi
import os
from charting import chart_base_path


def main(**kwargs):
    n = datetime.now()
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    files = list(filter(lambda x: 'stars_output' in x, files))
    files = list(filter(lambda x: x[:14].isdigit(), files))
    files = list(filter(lambda x: x[-4:] == "xlsx", files))
    date = [datetime.strptime(x[:14], "%Y%m%d%H%M%S") for x in files]
    min_date = [n - x for x in date]
    idx = min_date.index(min(min_date))
    file = files[idx]

    excel_file = pd.ExcelFile(file, engine='openpyxl')
    sector_table = excel_file.parse('OUTPUT_SHORT', index_col=0)
    total_df = excel_file.parse('OUTPUT_LONG', index_col=0)
    data_table = excel_file.parse('OUTPUT_ALL', index_col=0)

    index = sector_table.index.to_list()
    index.append('Score')
    sl = pd.IndexSlice[index]
    filename = f'{datetime.today().strftime("%d_%m_%Y")}_stars_all_data.jpeg'
    base = os.path.join("production")
    path = os.path.join(chart_base_path, base)
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    styled = total_df.style \
        .format(precision=2, decimal=',') \
        .apply(lambda x: ["font-weight: bold;" for v in x], axis=0, subset=(sl,)) \
        .map(lambda v: 'opacity: 40%;', subset=(pd.IndexSlice[data_table.index.to_list()],)) \
        .format_index(lambda x: x.replace('_', ' ').upper() if isinstance(x, str) else x, axis=0) \
        .apply_index(lambda x: np.where(x.isin(index), "font-weight: bold;", "font-weight: normal;"), axis=0)
    dfi.export(styled, filepath, table_conversion='playwright', dpi=200)


if __name__ == '__main__':
    main()
