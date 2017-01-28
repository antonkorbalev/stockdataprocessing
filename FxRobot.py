import oandapy
import matplotlib.pyplot as plt


token = open('Token.txt','r').read()
insName = 'EUR_USD'
maxLength=100

oanda = oandapy.API(environment="practice", access_token=token)
asks = list()
bids = list()

def get_prices():
    response = oanda.get_prices(instruments=insName)
    prices = response.get('prices')
    ask = prices[0].get('ask')
    bid = prices[0].get('bid')
    if len(asks) > 0 and len(bids) > 0:
        if asks[len(asks)-1]!=ask and bids[len(bids)-1]!=bid:
            asks.append(ask)
            bids.append(bid)
        else:
            print prices
    else:
        asks.append(ask)
        bids.append(bid)
    plt.clf()
    plt.plot(asks, label='ASK', color='red')
    plt.plot(bids, label='BID', color='green')
    plt.title(insName)
    plt.xlabel('Time, s')
    #plt.ylabel('Price '+ insName)
    plt.legend(loc='upper right')
    if (len(asks)>maxLength):
        asks.pop(0)
    if (len(bids) > maxLength):
        bids.pop(0)

plt.ion()
plt.grid(True)

while True:
    get_prices()
    plt.pause(0.05)


