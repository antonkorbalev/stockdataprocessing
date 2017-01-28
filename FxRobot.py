import oandapy
import matplotlib.pyplot as plt
from Config import Config

config = Config()
oanda = oandapy.API(environment="practice", access_token = config.token)
asks = list()
bids = list()
price_change = list()

def get_prices():
    response = oanda.get_prices(instruments=config.insName)
    prices = response.get('prices')
    ask = prices[0].get('ask')
    bid = prices[0].get('bid')
    status = prices[0].get('status')
    if status == 'halted':
        print config.insName, 'is halted.'
        return
    asks.append(ask)
    bids.append(bid)
    lastPrice = (asks[len(asks)-1] + bids[len(bids)-1]) / 2
    plt.clf()
    price_change.append((ask+bid)/2 - lastPrice)
    plt.plot(price_change, label='Price change', color='red')
    plt.title(config.insName)
    plt.xlabel('Time, s')
    plt.legend(loc='upper right')
    if (len(asks)>config.maxLength):
        asks.pop(0)
    if (len(bids) > config.maxLength):
        bids.pop(0)
    if (len(price_change) > config.maxLength):
        price_change.pop(0)

plt.ion()
plt.grid(True)

while True:
    get_prices()
    plt.pause(config.period)


