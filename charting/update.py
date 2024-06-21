import importlib
import os
from typing import List, Union


def get_files():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")
    file_list = os.listdir(path)

    return path, file_list


def update_charts(module_names: Union[List[str], List] = []) -> List[str]:
    path, file_list = get_files()
    errors = []
    charts_to_update = []
    incorrect_names = []
    if len(module_names) > 0:
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
                    module.main()
            except Exception as e:
                errors.append(module_name)

    return errors


if __name__ == '__main__':
    update_charts()

if __name__ == '__main__':
    errors = update_charts()
    for err in errors:
        print(err)