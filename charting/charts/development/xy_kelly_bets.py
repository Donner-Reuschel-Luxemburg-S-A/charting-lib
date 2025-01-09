import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.api import OLS
from scipy.stats import norm
import math
from matplotlib.ticker import MultipleLocator
from pandas import DateOffset
from source_engine.bloomberg_source import BloombergSource
from source_engine.fred_source import FredSource

from charting.model.chart import Chart
import matplotlib.dates as mdates

from charting.model.metadata import Metadata, Category, Region
from charting.transformer.lag import Lag
from charting.transformer.avg import Avg


def alpha_par(mu, var): # Alpha in the Beta distribution

    return mu*((mu*(1-mu)/var)-1)

def beta_par(mu, var): # Beta in the Beta distribution

    return (1-mu)*((mu*(1-mu)/var)-1)

def kelly_bet_size(p,theta):
    return ((p*theta-1)/(theta-1))


def kelly_unknown_p(delta,sigma):
    return 2*(delta**2-sigma**2)*norm.cdf(delta/sigma)+2*sigma*delta*norm.pdf(delta/sigma)

def kelly_bayes(x,n,a,b,theta):
    phat = (x+a)/(n+a+b)
    return ((phat*theta-1))/(theta-1)


def main():

    #mu1 etc der Prior (unconditional)

    #a = alpha_par(mu1,sigma1)
    #b = beta_par(mu2,sigma2)

    #print(a/(a+b))

    #x = 650
    #n = 1000

    #print(kelly_bet_size(0.55,2))

    #print(kelly_bayes(x,n,a,b,abs(mu2/mu1)+1))

    delta = 0.05
    sigma = 0.05

    #print(kelly_bet_size(0.65,2.25))

    print(kelly_unknown_p(delta,sigma))


if __name__ == '__main__':
    main()
