import getpass
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum


class Country(Enum):
    CN = "China"
    DE = "Germany"
    JP = "Japan"
    TW = "Taiwan"
    UK = "United Kingdom"
    US = "United States of America"


class Category(Enum):
    CURVES = "Curves"
    INFLATION = "Inflation"
    CONSUMER = "Consumer"
    EMPLOYMENT = "Employment"
    CREDIT = "Credit"
    ECONOMY = "Economy"


@dataclass
class Metadata:
    country: Country
    category: Category
    title: str
    author: str = getpass.getuser()
    date = str = datetime.today().strftime("%Y-%m-%d")

    def __iter__(self):
        for field, value in asdict(self).items():
            yield field, value



