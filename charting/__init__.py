"""
.. include:: ../README.md
"""

__version__ = "1.6.0"

import getpass
import os.path

from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from source_engine.indeed_source import IndeedSource

fred = FredSource()
indeed = IndeedSource()
try:
    blp = BloombergSource()
except Exception:
    blp = None

base_path = f"C:\\Users\\{getpass.getuser()}\\OneDrive - Donner Reuschel\\General - Portfolio Management\\Organisation Development"
chart_base_path = os.path.join(base_path, "charts")
ppt_base_path = os.path.join(base_path, "ppts")
