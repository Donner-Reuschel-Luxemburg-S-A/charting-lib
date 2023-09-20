"""
.. include:: ../README.md
"""

__version__ = "1.7.4"

import getpass
import os.path
user_path = f'C:\\Users\\{getpass.getuser()}'
base_path = f"{user_path}\\OneDrive - Donner Reuschel\\General - Portfolio Management\\Organisation Development"
chart_base_path = os.path.join(base_path, "charts")
ppt_base_path = os.path.join(user_path, "Downloads")
