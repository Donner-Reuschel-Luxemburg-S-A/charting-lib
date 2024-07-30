import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.api import OLS
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


def poisson(l, k): # poisson prob

    return math.pow(l,k) * math.exp(-l) / math.factorial(k)

def p_win(l1,l2,cut): # prob win 1st
    pwin = 0
    for i in range(0, cut):
        for j in range(i + 1, cut):
            pwin = pwin + poisson(l2, i)*poisson(l1, j)
    return pwin

def p_draw(l1,l2,cut): # prob draw
    pwin = 0
    for i in range(0, cut):
        pwin = pwin + poisson(l2, i) * poisson(l1, i)
    return pwin

def target_function(p1,p2,p3, l1,l2,cut): # squared diff
    return( (p1-p_win(l1,l2,cut))**2+(p2-p_draw(l1,l2,cut))**2+(p3-p_win(l2,l1,cut))**2)

def payoff(t1,t2,r1,r2):  # bet payoffs
    if(t1==r1 and t2 == r2):
        return 4
    elif (t1-t2 == r1-r2):
        return 3
    elif (np.sign(t1-t2) == np.sign(r1-r2)):
        return 2
    else:
        return 0

def expectedpayoff(t1,t2,l1,l2):
    e = 0
    for i in range(0,10):
        for j in range(0,10):
            e = e + payoff(t1,t2,i,j)*poisson(l1,i)*poisson(l2,j)
    return e





def optim(p1,p2,p3,cut): # grid optimizer, lambda 1 & 2
    x = 9999
    amin = 0
    bmin = 0
    for i in range(0,1000):
        for j in range(0,1000):
            t = target_function(p1,p2,p3,i/100,j/100,cut)
            if(t < x):
                x = t
                amin = i
                bmin = j
    return x, amin/100, bmin/100


def main():

    q1 = 2.2
    q2 = 3.1
    q3 = 3.5

    cut = 10

    p1 = (1 / q1) / (1 / q1 + 1 / q2 + 1 / q3)
    p2 = (1 / q2) / (1 / q1 + 1 / q2 + 1 / q3)
    p3 = (1 / q3) / (1 / q1 + 1 / q2 + 1 / q3)

    d = optim(p1,p2,p2,cut)

    l1 = d[1]
    l2 = d[2]


    Ausgabe = np.zeros((5,5))

    for i in range(0,5):
        for j in range(0,5):
            Ausgabe[i,j] = expectedpayoff(i,j,l1,l2)

    print(Ausgabe)

    print(Ausgabe.max())
    print(np.argmax(Ausgabe))









if __name__ == '__main__':
    main()
