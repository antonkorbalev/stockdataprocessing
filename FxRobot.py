import oandapy
import multiprocessing
import matplotlib.pyplot as plt
import numpy as np


token = open('Token.txt','r').read()
insName = 'EUR_USD'
maxLength=100

oanda = oandapy.API(environment="practice", access_token=token)
asks = list()
bids = list()

def get_prices():
    response = oanda.get_prices(instruments=insName)
    prices = response.get('prices')
    asks.append(prices[0].get('ask'))
    bids.append(prices[0].get('bid'))
    plt.clf()
    plt.plot(asks, label='ASK')
    plt.plot(bids, label='BID')
    plt.legend(loc='upper right')
    if (len(asks)>maxLength):
        asks.pop(0)
    if (len(bids) > maxLength):
        bids.pop(0)


plt.ion()


while True:
    get_prices()
    plt.pause(1)


