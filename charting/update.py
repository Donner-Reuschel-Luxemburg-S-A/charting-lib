import importlib
import os
from typing import List


def get_files():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")
    file_list = os.listdir(path)

    return path, file_list


def execute_main_methods() -> List[str]:
    path, file_list = get_files()
    errors = []

    for file_name in file_list:
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
    errors = execute_main_methods()

    for error in errors:
        print(error)
