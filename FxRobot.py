import oandapy
import matplotlib.pyplot as plt
from Config import Config
from os import path
import datetime

config = Config()
oanda = oandapy.API(environment="practice", access_token = config.token)
asks = list()
bids = list()
price_change = list()
f_back_log = open(path.relpath(config.back_log_path + '/' + config.insName + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))+'.log', 'a');
if config.write_back_log:
    print 'Backlog file name:', f_back_log.name
    f_back_log.write('DateTime,Instrument,ASK,BID,Status \n')

def get_prices():
    response = oanda.get_prices(instruments=config.insName)
    prices = response.get('prices')
    ask = prices[0].get('ask')
    bid = prices[0].get('bid')
    status = prices[0].get('status')
    if status == 'halted':
        print config.insName, 'is halted.'
        return
    f_back_log.write('%s,%s,%s,%s,%s \n' % (datetime.datetime.now(), config.insName, prices[0].get('ask'), prices[0].get('bid'), prices[0].get('status')))
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


