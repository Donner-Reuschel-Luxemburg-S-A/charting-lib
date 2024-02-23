import importlib
import os
from typing import List, Union


def get_files():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")
    file_list = os.listdir(path)

    return path, file_list


def execute_main_methods(names: Union[List[str], List] = []) -> List[str]:
    path, file_list = get_files()
    errors = []
    charts_to_update = []
    incorrect_names = []
    if len(names) > 0:
        for chart in names:
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
            module = importlib.import_module(f'charting.charts.production.{module_name}')

            if hasattr(module, 'main') and callable(getattr(module, 'main')):
                try:
                    module.main()
                except Exception as e:
                    errors.append(module_name)

    return errors


def update(module: str):
    module = importlib.import_module(module)

    if hasattr(module, 'main') and callable(getattr(module, 'main')):
        module.main()


if __name__ == "__main__":
    l = ['eu_sxfivee_sxxp_mcxp_scxp_yield_six_month', 'eu_sxxp_yield_six_month', 'eu_sxxp_sector_per_overview', 'eu_indices_per_overview']
    errors = execute_main_methods(l)

    for error in errors:
        print(error)
