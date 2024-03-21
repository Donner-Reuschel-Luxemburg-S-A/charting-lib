import time

from source_engine.estat_statistics import EstatStatisticsSource
from source_engine.imf_source import ImfSource

countries = ['DE', 'IT', 'FR', 'FI', 'NL', 'BE', 'AT', 'ES', 'PT']
period = 'A'
series = [('FM', 'GGXONLB_G01_GDP_PT'), ('FM', 'GGXCNL_G01_GDP_PT'), ('IFS', 'RAFA_USD')]

src = ImfSource()
estat_source = EstatStatisticsSource()
estat_queries = ['tipsun30?format=JSON&sinceTimePeriod=2003-Q1&unit=PC_ACT&s_adj=SA&sex=T&age=Y15-74&lang=en',
'gov_10q_ggdebt?format=JSON&sinceTimePeriod=1994-Q4&unit=PC_GDP&na_item=GD&sector=S13&lang=en',
'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ESI-I&s_adj=SA&lang=en',
'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ICI-BAL&s_adj=SA&lang=en'
                 ]

estat_results = []
for query in estat_queries:
    estat_results.append(estat_source.get_data(query))
output = {}
for c in countries:
    output[c] = {}
    for dataset, s in series:
        output[c][s] = src.fetch_data(series=dataset, params=f'{period}.{c}.{s}')
        time.sleep(1)
