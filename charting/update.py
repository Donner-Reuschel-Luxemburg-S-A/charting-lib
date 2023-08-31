import os
import importlib


def execute_main_methods():
    path = os.path.join(os.path.dirname(__file__), "charts", "production")

    file_list = os.listdir(path)

    for file_name in file_list:
        if file_name.endswith('.py') and file_name != "__init__.py":
            module_name = file_name[:-3]
            module = importlib.import_module(f'charting.charts.production.{module_name}')

            if hasattr(module, 'main') and callable(getattr(module, 'main')):
                module.main()


def update(module: str):
    module = importlib.import_module(module)

    if hasattr(module, 'main') and callable(getattr(module, 'main')):
        module.main()


if __name__ == "__main__":
    execute_main_methods()
