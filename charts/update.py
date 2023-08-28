import os
import importlib


def execute_main_methods():
    path = os.path.join(os.getcwd(), "production")

    file_list = os.listdir(path)

    for file_name in file_list:
        if file_name.endswith('.py'):
            module_name = file_name[:-3]
            module = importlib.import_module(f'charts.production.{module_name}')

            if hasattr(module, 'main') and callable(getattr(module, 'main')):
                print(f"Executing main method from {module_name}")
                module.main()


if __name__ == "__main__":
    execute_main_methods()
