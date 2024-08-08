import importlib
import os
from typing import List, Union


def get_files():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")
    file_list = os.listdir(path)

    return path, file_list


def update_charts(module_names: Union[List[str], List]) -> List[str]:
    path, file_list = get_files()
    errors = []
    charts_to_update = []
    incorrect_names = []
    if module_names and len(module_names) > 0:
        for chart in module_names:
            if not chart.endswith('py'):
                chart = chart + '.py'
            try:
                charts_to_update.append(file_list[file_list.index(chart)])
            except ValueError:
                incorrect_names.append(chart)
    else:
        charts_to_update = file_list

    for file_name in charts_to_update:
        if (file_name.endswith('.py') or file_name.endswith('.pyc')) and file_name != "__init__.py":
            module_name = os.path.splitext(file_name)[0]

            try:
                module = importlib.import_module(f'charting.charts.production.{module_name}')

                if hasattr(module, 'main') and callable(getattr(module, 'main')):
                    module.main(language="en")
                    module.main(language="de")
            except Exception as e:
                errors.append(module_name)

    return errors


if __name__ == '__main__':
    errors = update_charts(module_names=[
    "global_asset_class_yield",
    "de_gov_ecb_yields",
    "eu_periphery_spreads",
    "eu_euroagg_securitized_agency",
    "eu_ig_credit_spread",
    "eu_performance",
    "eu_performance_sektoren",
    "global_equity_indices_yield",
    "eu_sxxp_sector_performance",
    "us_spx_sector_performance",
    "global_indices_per_overview",
    "eu_us_sxxp_spx_per",
    "eu_sxxp_profits_quarterly",
    "us_spx_profits_quarterly",
    "us_vix_vtwox",
    "global_cmdty_index",
    "global_wti_brent_oil",
    "global_gold",
    "global_silver",
    "currency_eur_usd",
    "currency_eur_gbp",
    "currency_eur_chf",
    "currency_eur_jpy",
    "portfolio_allocation",
    "bond_allocation_2",
    "bond_allocation",
    "duration_history",
    "equity_ratio",
    "equity_sector_country",
    "global_key_interest_rates+pricing",
    "de_cpi_ppi",
    "eu_inflation_cpi_pmi",
    "eu_memb_gdp",
    "eu_memb_unemployment",
    "eu_memb_industrial_production",
    "eu_memb_retail_sales",
    "de_ifo_business_climate",
    "de_zew_business_climate",
    "eu_citi",
    "global_central_banks",
    "eu_yield_curves_gov_cov",
    "eur_expected_returns",
    "de_linker",
    "eu_core_spreads",
    "eu_semicore_spreads",
    "eu_sxxp_mvag",
    "us_spx_mvag",
    "us_spx_put_call_ratio",
    "global_mxef_mxwo_per",
    "eu_us_sxxp_spx_profit_margin",
    "global_profit_minus_ten_year_profit"
])
    for err in errors:
        print(err)
