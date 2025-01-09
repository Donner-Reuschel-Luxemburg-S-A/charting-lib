import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.api import OLS
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource
from statsmodels.tsa.stattools import adfuller

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def calculate_drawdowns(series: pd.Series, drawdown_threshold: float, recovery_threshold: float) -> pd.Series:
    """
    Calculate drawdown and recovery events in a time series. After a drawdown of the specified threshold occurs,
    the drawdown state is triggered. Recovery occurs when the price reaches the pre-drawdown price or makes a new high.
    Args:
    - series (pd.Series): Time series of price data.
    - drawdown_threshold (float): The percentage decline required to trigger a drawdown.
    - recovery_threshold (float): The percentage required for a price to recover.
    Returns:
    - pd.Series: A series marking points where drawdowns or recoveries occurred (event types: "drawdown", "recovery").
    """
    in_drawdown = False
    peak_price = series.iloc[0]  # Track the highest price
    initial_drawdown_price = None  # Price before the first drawdown
    trough_price = None  # Track the lowest point during a drawdown
    event_types = pd.Series([None] * len(series), index=series.index)  # Initialize the event types series
    for i in range(0, len(series)):
        current_price = series.iloc[i]
        # If not in a drawdown state, check if the current price sets a new peak
        if not in_drawdown:
            if current_price > peak_price:
                peak_price = current_price
                logging.info(f"New peak at {series.index[i]} with price {current_price}")
            else:
                # Calculate the drawdown from the peak
                price_change_from_peak = (current_price - peak_price) / peak_price * 100
                logging.info(f"current drawdown {series.index[i]} with {price_change_from_peak}%")
                if price_change_from_peak <= -drawdown_threshold:
                    logging.info(f"Drawdown triggered at {series.index[i]} with price {current_price}")
                    in_drawdown = True
                    initial_drawdown_price = current_price * (1 + recovery_threshold / 100)  # Set recovery target
                    trough_price = current_price  # Set the initial trough price
                    event_types.iloc[i] = "drawdown"
        else:
            # If in drawdown, track further drawdowns based on the drawdown threshold from the trough price
            price_change_from_trough = (current_price - trough_price) / trough_price * 100
            if price_change_from_trough <= -drawdown_threshold:
                logging.info(f"Further drawdown detected at {series.index[i]} with price {current_price}")
                initial_drawdown_price = current_price * (1 + recovery_threshold / 100)
                trough_price = current_price
                event_types.iloc[i] = "drawdown"
            # Check if recovery occurs
            # Recovery Scenario 1: Price exceeds previous peak (new high)
            if current_price > peak_price:
                logging.info(f"Recovery by new peak triggered at {series.index[i]} with price {current_price}")
                in_drawdown = False
                peak_price = current_price  # New peak is set
                initial_drawdown_price = None
                trough_price = None
                event_types.iloc[i] = "recovery"
            # Recovery Scenario 2: Price reaches or exceeds the initial drawdown price
            elif initial_drawdown_price is not None and current_price >= initial_drawdown_price:
                logging.info(
                    f"Recovery by returning to initial drawdown price at {series.index[i]} with price {current_price}")
                in_drawdown = False
                # TODO: Need to be checked
                peak_price = max(current_price, peak_price)  # Reset peak price if necessary
                initial_drawdown_price = None
                trough_price = None
                event_types.iloc[i] = "recovery"
    return event_types


def compute_quantiles(df):


    return 0


if __name__ == '__main__':

    prices = pd.read_excel("C:\\Users\\tregele\\OneDrive - Donner Reuschel\\Test_RoIC.xlsx", sheet_name="SPX", header=0, index_col=0, parse_dates=True)

    returns = prices.pct_change()

    roic = pd.read_excel("C:\\Users\\tregele\\OneDrive - Donner Reuschel\\Test_RoIC.xlsx", sheet_name="RoIC", header=0, index_col=0, parse_dates=True)



