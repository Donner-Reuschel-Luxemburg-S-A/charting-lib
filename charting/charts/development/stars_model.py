import time
from scipy.stats import zscore
from source_engine.estat_statistics import EstatStatisticsSource
from source_engine.imf_source import ImfSource
from source_engine.sdmx_source import Ecb

countries = ['DE', 'IT', 'FR', 'FI', 'NL', 'BE', 'AT', 'ES', 'PT']
period = 'A'
imf_queries = [('FM', 'GGXONLB_G01_GDP_PT'), ('FM', 'GGXCNL_G01_GDP_PT'), ('IFS', 'RAFA_USD')]

src = ImfSource()
ecb_source = Ecb()
estat_source = EstatStatisticsSource()


estat_queries = [
'tipsun30?format=JSON&sinceTimePeriod=2003-Q1&unit=PC_ACT&s_adj=SA&sex=T&age=Y15-74&lang=en',
'gov_10q_ggdebt?format=JSON&sinceTimePeriod=1994-Q4&unit=PC_GDP&na_item=GD&sector=S13&lang=en',
'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ESI-I&s_adj=SA&lang=en',
'ei_bssi_m_r2?format=JSON&sinceTimePeriod=2000-01&indic=BS-ICI-BAL&s_adj=SA&lang=en',
'bop_gdp6_q?format=JSON&freq=Q&sinceTimePeriod=2000-Q1&unit=PC_GDP&partner=WRL_REST&stk_flow=BAL&s_adj=NSA&bop_item=CA&lang=en',
'bop_gdp6_q?format=JSON&freq=Q&sinceTimePeriod=2000-Q1&unit=PC_GDP&partner=WRL_REST&stk_flow=N_LE&s_adj=NSA&bop_item=FA&lang=en',
'ei_lmlc_q?format=JSON&sinceTimePeriod=2000-Q1&unit=I20&p_adj=NV&s_adj=SCA&nace_r2=B-N&indic=LM-LCI-TOT&lang=en',
'tec00131?format=JSON&sinceTimePeriod=2011&unit=PC&na_item=SRG_S14_S15&sector=S14_S15&lang=en'
                 ]

ecb_queries = {'W0.67._Z._Z.A.A.I3006._Z._Z._Z._Z._Z._Z.PC':
    [
        ('CBD2', f'Q.{c}.W0.67._Z._Z.A.A.I3006._Z._Z._Z._Z._Z._Z.PC')
        for c in countries
     ]
}
ecb_queries.extend([
    ('CBD2', f'Q.{c}.W0.67._Z._Z.A.F.A1131._X.ALL.CA._Z.LE._T.EUR')
    for c in countries
])

ecb_result = []
for query in ecb_queries:
    ecb_result.append(ecb_source.get_data(*query))

estat_results = []
for query in estat_queries:
    estat_results.append(estat_source.get_data(query))

imf_result = {}
for c in countries:
    imf_result[c] = {}
    for dataset, s in imf_queries:
        imf_result[c][s] = src.fetch_data(series=dataset, params=f'{period}.{c}.{s}')
        time.sleep(1)
