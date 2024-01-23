import getpass
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import List, Union


class Region(Enum):
    GLOBAL = "Global"
    EU = "Europe"
    EM = "Emerging Markets"
    CN = "CN"
    DE = "DE"
    CH = "CH"
    JP = "JP"
    TW = "TW"
    UK = "UK"
    US = "US"
    AU = "AU"
    NO = "NO"
    CA = "CA"
    SE = "SE"
    NZ = "NZ"
    IN = "IN"
    SG = "SG"
    ZA = "ZA"
    TR = "TR"


class Category(Enum):
    RATES = "Rates"
    INFLATION = "Inflation"
    CONSUMER = "Consumer"
    EMPLOYMENT = "Employment"
    CREDIT = "Credit"
    ECONOMY = "Economy"
    COMMODITY = "Commodity"
    EQUITY = "Equity"
    SURVEY = "Survey"
    CB = "Central Banks"
    VOLATILITY = "Volatility"
    FI = "Fixed Income"
    FX = "Forex"
    ALTERNATIVES = "Alternatives"


@dataclass
class Metadata:
    region: Union[Region, List[Region]]
    category: Union[Category, List[Category]]
    title: str
    author: str = getpass.getuser()
    date = str = datetime.today().strftime("%Y-%m-%d")

    def __post_init__(self):
        if not isinstance(self.region, list):
            self.region = [self.region]
        if not isinstance(self.category, list):
            self.category = [self.category]

    def __iter__(self):
        for field, value in asdict(self).items():
            yield field, value



