import os
from datetime import datetime, timedelta

import pandas as pd


def at1_bonds():
    path = os.path.join(os.path.dirname(__file__),  "..", "data", "Subordinate.xlsx")
    issuer = ['DB', 'SANTAN', 'UCGIM', 'ISPIM', 'RABOBK', 'CMZB', 'BKIR', 'SOGEN']
    df = pd.read_excel(path,
                       sheet_name="AT1", index_col="security_des().value", header=0, parse_dates=['issue_dt().value',
                                                                                                  'nxt_call_dt()',
                                                                                                  'first_call_dt_issuance().value']).iloc[
         :, :12]
    df.columns = ['ID', 'YTC', 'YTM', 'CPN', 'ISSUE_DT', 'NEXT_CALL_DT', 'FIRST_CALL_DT', 'RTG', 'RESET_SPREAD',
                  'REST_INDEX', 'RESET_RATE', 'SWAP_TO_CALL']
    df['RESET_CPN'] = df['RESET_SPREAD'] / 100 + df['RESET_RATE']
    df['CREDIT_SPREAD'] = df['YTC'] - df['SWAP_TO_CALL']
    df['TICKER'] = pd.Series(df.reset_index()['security_des().value'].apply(lambda x: x.split()[0]).values,
                             index=df.index)
    df['YEARS_TO_CALL'] = (df['NEXT_CALL_DT'] - pd.Timestamp(datetime.today().date())).dt.days / 365
    df['CLOSEST_TO_5'] = (df['YEARS_TO_CALL'] - 5).abs()

    df = df.dropna()
    df = df[df.index.to_series().apply(lambda x: 'Float PERP' not in x)]
    df = df[df.index.to_series().apply(lambda x: x.split(' ')[0] in issuer)]

    sd_max = df['YTM'].std() * 3 + df['YTM'].mean()
    sd_min = df['YTM'].std() * -3 + df['YTM'].mean()
    df = df[(sd_min < df['YTM']) & (sd_max > df['YTM'])]
    sd_max = df['YTC'].std() * 3 + df['YTC'].mean()
    sd_min = df['YTC'].std() * -3 + df['YTC'].mean()
    df = df[(sd_min < df['YTC']) & (sd_max > df['YTC'])]
    df = df[df['ISSUE_DT'] > pd.Timestamp(datetime.today().date() + timedelta(days=-4 * 365))]
    df_reset = df.loc[df.groupby('TICKER')['CLOSEST_TO_5'].idxmin()]

    def helper(x):
        filter_ = df_reset['TICKER'] == x['TICKER']
        return df_reset[filter_]['CREDIT_SPREAD'].iloc[0]

    df['5Y_CREDIT_SPREAD'] = df.apply(helper, axis=1) * 100
    return df

def non_fin_bonds():
    path = os.path.join(os.path.dirname(__file__),  "..", "data", "Subordinate.xlsx")
    df = pd.read_excel(path,
                       sheet_name="NON-FIN", index_col="security_des().value", header=0,
                       parse_dates=[
                                    'nxt_call_dt().value']
                       )
    df.columns = ['ID', 'YTC', 'NEXT_CALL_DT']
    df['TICKER'] = pd.Series(df.reset_index()['security_des().value'].apply(lambda x: x.split()[0]).values,
                             index=df.index)
    df['YEARS_TO_CALL'] = (df['NEXT_CALL_DT'] - pd.Timestamp(datetime.today().date())).dt.days / 365
    df = df[df['NEXT_CALL_DT'] > pd.Timestamp(datetime.now().date() + timedelta(days=360))]
    df = df.sort_values(['TICKER', 'NEXT_CALL_DT'])
    return df