import oandapyV20
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20.endpoints.accounts import AccountDetails
import oandapyV20.endpoints.positions as positions
import matplotlib.pyplot as plt
from Config import Config
from os import path
import datetime
import numpy

config = Config()
oanda = oandapyV20.API(environment='practice', access_token = config.token)
pReq = PricingInfo(config.account_id, 'instruments='+config.insName)

asks = list()
bids = list()
price_change = list()
if config.write_back_log:
    f_back_log = open(path.relpath(config.back_log_path + '/' + config.insName + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))+'.log', 'a');
time = 0
times = list()
last_result = 'hold'
deals = list()
deal_price = 0
max_spread = 0
min_spread = 1
plusDeals = 0
minusDeals = 0
meanDeals = 0

if config.write_back_log:
    print 'Backlog file name:', f_back_log.name
    f_back_log.write('DateTime,Instrument,ASK,BID,Price change,Status, Spread, Result \n')

def process_data(ask, bid, status):
    global last_result
    global deal_price
    global plusDeals
    global minusDeals
    global meanDeals
    global max_spread
    global min_spread
    if status != 'tradeable':
        print config.insName, 'is halted.'
        return
    asks.append(ask)
    bids.append(bid)
    lastPrice = (ask+bid)/2
    if (len(asks) > 1) and (len(bids) > 1):
        lastPrice = (asks[len(asks)-2] + bids[len(bids)-2]) / 2
    pChange = (ask+bid)/2 - lastPrice
    price_change.append(pChange)
    result = 'hold'
    plt.clf()
    times.append(time)
    hmin = 0
    hmax = 0
    plt.subplot(2,1,1)
    if len(price_change) > 3:
        hmaxs = list()
        for i in range(1, len(price_change) - 2):
            if price_change[i] > price_change[i-1] and price_change[i] > price_change[i+1]:
                hmaxs.append(price_change[i])
        if len(hmaxs) > 0:
            hmax = numpy.mean(hmaxs)
            plt.axhline(y=hmax, label='MAX', color='red', linestyle=':')
        hmins = list()
        for i in range(1, len(price_change) - 2):
            if price_change[i] < price_change[i-1] and price_change[i] < price_change[i+1]:
                hmins.append(price_change[i])
        if len(hmins) > 0:
            hmin = numpy.mean(hmins)
            plt.axhline(y=hmin, label='MIN', color='green', linestyle=':')
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

    plt.subplot(2,2,3)
    plt.hist(deals,color='blue')
    spread = ask - bid
    if max_spread < spread :
        max_spread = spread
    if min_spread > spread:
        min_spread = spread
    plt.axvline(x = spread, color='red')
    plt.axvline(x = max_spread, color='gray', linestyle=":")
    plt.axvline(x = min_spread, color='gray', linestyle=":")
    plt.ylabel('Count of deals')
    plt.xticks([])

    plt.subplot(2, 2, 4)
    totalDeals = minusDeals + meanDeals + plusDeals
    if totalDeals!=0:
        plt.bar(0, 100 * float(minusDeals)/float(totalDeals), color='red')
        plt.bar(1, 100 * float(meanDeals)/float(totalDeals), color='blue')
        plt.bar(2, 100 * float(plusDeals)/float(totalDeals), color='green')
    plt.xticks([0,1,2], ['Minus', 'Mean', 'Plus'])
    plt.ylabel('% of deals')
    plt.margins(0.1)

    if len(asks) > config.maxLength:
        asks.pop(0)
    if len(bids) > config.maxLength:
        bids.pop(0)
    if len(price_change) > config.maxLength:
        price_change.pop(0)
    if len(times) > config.maxLength:
        times.pop(0)

    plt.tight_layout()

    if result != 'hold':
        diff = 0
        if last_result == 'buy':
                diff = pChange - deal_price
        if last_result == 'sell':
                diff = deal_price - pChange
        if diff != 0:
            deals.append(diff)
            if diff >= max_spread:
                plusDeals = plusDeals + 1
            if diff <= min_spread:
                minusDeals = minusDeals + 1
            if diff > min_spread and diff < max_spread :
                meanDeals = meanDeals + 1
        last_result = result
        deal_price = pChange
    if config.write_back_log:
        f_back_log.write('%s,%s,%s,%s,%s,%s,%s \n' % (datetime.datetime.now(), config.insName, pReq.response.get('prices')[0].get('asks')[1].get('price'), pReq.response.get('prices')[0].get('bids')[1].get('price'), pChange, ask-bid, result))
    print time, "s : ", result, ' spread size: ', ask - bid
    return result

def do_long(ask):
    if config.take_profit_value!=0 or config.stop_loss_value!=0:
        mktOrder = MarketOrderRequest(instrument=config.insName,
                                      units=config.lot_size,
                                      takeProfitOnFill=TakeProfitDetails(price=ask+config.take_profit_value).data,
                                      stopLossOnFill=StopLossDetails(price=ask-config.stop_loss_value).data)
    else:
        mktOrder = MarketOrderRequest(instrument=config.insName,
                                      units=config.lot_size)
    r = orders.OrderCreate(config.account_id, data=mktOrder.data)
    oanda.request(r)
    print r.response

def do_short(bid):
    if config.take_profit_value!=0 or config.stop_loss_value!=0:
        mktOrder = MarketOrderRequest(instrument=config.insName,
                                      units=-config.lot_size,
                                      takeProfitOnFill=TakeProfitDetails(price=ask+config.take_profit_value).data,
                                      stopLossOnFill=StopLossDetails(price=ask-config.stop_loss_value).data)
    else:
        mktOrder = MarketOrderRequest(instrument=config.insName,
                                      units=config.lot_size)
    r = orders.OrderCreate(config.account_id, data=mktOrder.data)
    oanda.request(r)
    print r.response

def do_close():
    try:
        r = positions.PositionClose(config.account_id, 'EUR_USD', {"longUnits": "ALL"})
        resp = oanda.request(r)
        print resp
    except:
        print 'No long units to close'
    try:
        r = positions.PositionClose(config.account_id, 'EUR_USD', {"shortUnits": "ALL"})
        resp = oanda.request(r)
        print resp
    except:
        print 'No short units to close'

def get_bal():
    r = AccountDetails(config.account_id)
    return oanda.request(r).get('account').get('balance')

plt.ion()
plt.grid(True)

while True:
    try:
        oanda.request(pReq)
        # max ask
        ask = float(pReq.response.get('prices')[0].get('asks')[1].get('price'))
        # min bid
        bid = float(pReq.response.get('prices')[0].get('bids')[1].get('price'))
        status = pReq.response.get('prices')[0].get('status')
        result = process_data(ask, bid, status)
        if plusDeals != 0 or minusDeals != 0:
            success = 100 * float(plusDeals)/float(meanDeals+plusDeals+minusDeals)
            print 'Success percent:', success, '%'
            if success < config.percent_of_success:
                print 'No success. Skip step. Take stats.'
                do_close()
            else:
                if result == 'buy':
                    do_long(ask)
                if result == 'sell':
                    do_short(bid)
                if result == 'close':
                    do_close()
        print 'Current balance:', get_bal()

    except Exception as e:
        print e
    plt.pause(config.period)
    time = time + config.period


