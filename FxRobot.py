import oandapy
import matplotlib.pyplot as plt


token = open('Token.txt','r').read()
insName = 'EUR_USD'
maxLength=100 # ticks
period = 1 #s

oanda = oandapy.API(environment="practice", access_token=token)
asks = list()
bids = list()
price_change = list()

def get_prices():
    response = oanda.get_prices(instruments=insName)
    prices = response.get('prices')
    ask = prices[0].get('ask')
    bid = prices[0].get('bid')
    status = prices[0].get('status')
    if status == 'halted':
        print insName, 'is halted.'
        return
    asks.append(ask)
    bids.append(bid)
    lastPrice = (asks[len(asks)-1] + bids[len(bids)-1]) / 2
    plt.clf()
    price_change.append((ask+bid)/2 - lastPrice)
    plt.plot(price_change, label='Price change', color='red')
    #plt.plot(asks, label='ASK', color='red')
    #plt.plot(bids, label='BID', color='green')
    plt.title(insName)
    plt.xlabel('Time, s')
    #plt.ylabel('Price '+ insName)
    plt.legend(loc='upper right')
    if (len(asks)>maxLength):
        asks.pop(0)
    if (len(bids) > maxLength):
        bids.pop(0)
    if (len(price_change) > maxLength):
        price_change.pop(0)

plt.ion()
plt.grid(True)

while True:
    get_prices()
    plt.pause(period)


