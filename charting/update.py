import os
import importlib


def execute_main_methods():
    path = os.path.join(os.getcwd(), "production")

    file_list = os.listdir(path)

    for file_name in file_list:
        if file_name.endswith('.py') and file_name != "__init__.py":
            module_name = file_name[:-3]
            try:
                module = importlib.import_module(f'charts.production.{module_name}')

                if hasattr(module, 'main') and callable(getattr(module, 'main')):
                    module.main()
            except Exception as e:
                print(f"Could not update chart {module_name}. Please update it manually.")


def update(module: str):
    module = importlib.import_module(module)

    if hasattr(module, 'main') and callable(getattr(module, 'main')):
        module.main()


if __name__ == "__main__":
    update("charts.production.global_indeed_job_postings")
