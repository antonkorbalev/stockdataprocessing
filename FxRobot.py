import oandapy
import matplotlib.pyplot as plt
from Config import Config
from os import path
import datetime
import numpy

config = Config()
oanda = oandapy.API(environment="practice", access_token = config.token)
asks = list()
bids = list()
price_change = list()
f_back_log = open(path.relpath(config.back_log_path + '/' + config.insName + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))+'.log', 'a');
time = 0
times = list()
last_result = 'hold'

if config.write_back_log:
    print 'Backlog file name:', f_back_log.name
    f_back_log.write('DateTime,Instrument,ASK,BID,Price change,Status \n')

def get_real_prices():
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
    lastPrice = (ask+bid)/2
    if (len(asks) > 1) and (len(bids) > 1):
        lastPrice = (asks[len(asks)-2] + bids[len(bids)-2]) / 2
    pChange = (ask+bid)/2 - lastPrice
    price_change.append(pChange)
    if config.write_back_log:
        f_back_log.write('%s,%s,%s,%s,%s,%s \n' % (datetime.datetime.now(), config.insName, prices[0].get('ask'), prices[0].get('bid'), pChange, prices[0].get('status')))
    result = process_data(price_change)
    global last_result
    if result != 'hold':
        last_result = result
    print time, "s : ", result, ' spread size: ', ask - bid

def process_data(price_change):
    result = 'hold'
    global last_result
    plt.clf()
    times.append(time)
    hmin = 0
    hmax = 0
    if len(price_change) > 3:
        hmaxs = list()
        for i in range(1, len(price_change) - 2):
            if price_change[i] > price_change[i-1] and price_change[i] > price_change[i+1]:
                hmaxs.append(price_change[i])
        if len(hmaxs) > 0:
            hmax = numpy.mean(hmaxs)
            plt.plot([times[0],times[len(times)-1]], [hmax, hmax], label='MAX', color='red', linestyle=':')
        hmins = list()
        for i in range(1, len(price_change) - 2):
            if price_change[i] < price_change[i-1] and price_change[i] < price_change[i+1]:
                hmins.append(price_change[i])
        if len(hmins) > 0:
            hmin = numpy.mean(hmins)
            plt.plot([times[0],times[len(times)-1]], [hmin, hmin], label='MIN', color='green', linestyle=':')
    if hmin != 0 and hmax != 0:
        if price_change[len(price_change)-1] >= hmax:
            if last_result != 'sell':
                result = 'sell'
        if price_change[len(price_change)-1] <= hmin:
            if last_result != 'buy':
                result = 'buy'
        if price_change[len(price_change) - 1] > hmin and price_change[len(price_change)-1] < hmax:
            if last_result != 'close' and last_result!='hold':
                result = 'close'

    plt.plot(times, price_change, label='Price change', color='blue',  marker='')
    plt.title(config.insName)
    plt.xlabel('Time, s')

    plt.legend(loc='upper left')
    if len(asks) > config.maxLength:
        asks.pop(0)
    if len(bids) > config.maxLength:
        bids.pop(0)
    if len(price_change) > config.maxLength:
        price_change.pop(0)
    if len(times) > config.maxLength:
        times.pop(0)

    return result


plt.ion()
plt.grid(True)

while True:
    get_real_prices()
    plt.pause(config.period)
    time = time + config.period


