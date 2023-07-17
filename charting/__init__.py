"""
.. include:: ../README.md
"""

__version__ = "1.4.2"

import getpass

from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

fred = FredSource()
blp = BloombergSource()

base_path = f"C:\\Users\\{getpass.getuser()}\\OneDrive - Donner Reuschel\\General - Portfolio Management\\Organisation Development\\charts"
