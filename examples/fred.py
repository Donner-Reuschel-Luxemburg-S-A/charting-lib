from typing import Any

import fredapi as fa
import pandas as pd


fred = fa.Fred(api_key='f811bd5632e04f215e8ae4a236bcaa90')


def get_data(series_id: str, observation_start: Any = None):
    if observation_start is not None:
        data = fred.get_series(series_id, observation_start=observation_start)
    else:
        data = fred.get_series(series_id)
    info = fred.get_series_info(series_id)
    df = pd.DataFrame({'y': data})
    return df, info.title, f'{info.units} [{info.units_short}]'
