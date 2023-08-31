import os
import importlib


def get_files():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")
    file_list = os.listdir(path)

    return path, file_list


def execute_main_methods():
    path, file_list = get_files()

    for file_name in file_list:
        if (file_name.endswith('.py') or file_name.endswith('.pyc')) and file_name != "__init__.py":
            module_name = os.path.splitext(file_name)[0]
            module = importlib.import_module(f'charting.charts.production.{module_name}')

            if hasattr(module, 'main') and callable(getattr(module, 'main')):
                module.main()


def update(module: str):
    module = importlib.import_module(module)

    if hasattr(module, 'main') and callable(getattr(module, 'main')):
        module.main()


if __name__ == "__main__":
    execute_main_methods()
