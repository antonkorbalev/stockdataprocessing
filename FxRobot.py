import datetime
from datetime import datetime
from os import path

import matplotlib.pyplot as plt
import oandapyV20
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails
from oandapyV20.endpoints.accounts import AccountDetails
from oandapyV20.endpoints.pricing import PricingInfo
from Conf.Config import Config
import seaborn

config = Config()
oanda = oandapyV20.API(environment=config.env, access_token = config.token)
pReq = PricingInfo(config.account_id, 'instruments='+config.insName)

asks = list()
bids = list()
long_time = datetime.now()
short_time = datetime.now()

if config.write_back_log:
    f_back_log = open(path.relpath(config.back_log_path + '/' + config.insName + '_' + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))+'.log', 'a');
time = 0
times = list()
last_ask = 0
last_bid = 0

if config.write_back_log:
    print 'Backlog file name:', f_back_log.name
    f_back_log.write('DateTime,Instrument,ASK,BID,Price change,Status, Spread, Result \n')

def process_data(ask, bid, status):
    global last_result
    global last_ask
    global last_bid
    global  long_time
    global short_time
    if status != 'tradeable':
        print config.insName, 'is halted.'
        return
    asks.append(ask)
    bids.append(bid)
    times.append(time)

    # --- begin strategy here ---



    # --- end strategy here ---

    if len(asks) > config.maxLength:
        asks.pop(0)
    if len(bids) > config.maxLength:
        bids.pop(0)
    if len(times) > config.maxLength:
        times.pop(0)

    if config.write_back_log:
        f_back_log.write('%s,%s,%s,%s,%s,%s,%s \n' % (datetime.datetime.now(), config.insName, pReq.response.get('prices')[0].get('asks')[1].get('price'), pReq.response.get('prices')[0].get('bids')[1].get('price'), pChange, ask-bid, result))

def do_long(ask):
    if config.take_profit_value!=0 or config.stop_loss_value!=0:
        order = MarketOrderRequest(instrument=config.insName,
                                      units=config.lot_size,
                                      takeProfitOnFill=TakeProfitDetails(price=ask+config.take_profit_value).data,
                                      stopLossOnFill=StopLossDetails(price=ask-config.stop_loss_value).data)
    else:
        order = MarketOrderRequest(instrument=config.insName,
                                      units=config.lot_size)
    r = orders.OrderCreate(config.account_id, data=order.data)
    resp = oanda.request(r)
    print resp
    price = resp.get('orderFillTransaction').get('price')
    print time, 's: BUY price =', price
    return float(price)

def do_short(bid):
    if config.take_profit_value!=0 or config.stop_loss_value!=0:
        order = MarketOrderRequest(instrument=config.insName,
                                      units=-config.lot_size,
                                      takeProfitOnFill=TakeProfitDetails(price=bid+config.take_profit_value).data,
                                      stopLossOnFill=StopLossDetails(price=bid-config.stop_loss_value).data)
    else:
        order = MarketOrderRequest(instrument=config.insName,
                                      units=-config.lot_size)
    r = orders.OrderCreate(config.account_id, data=order.data)
    resp = oanda.request(r)
    print resp
    price = resp.get('orderFillTransaction').get('price')
    print time, 's: SELL price =', price
    return float(price)

def do_close_long():
    try:
        r = positions.PositionClose(config.account_id, 'EUR_USD', {"longUnits": "ALL"})
        resp = oanda.request(r)
        print resp
        pl = resp.get('longOrderFillTransaction').get('pl')
        real_profits.append(float(pl))
        print time, 's: Closed. Profit = ', pl, ' price = ', resp.get('longOrderFillTransaction').get('price')
    except:
        print 'No long units to close'

def do_close_short():
    try:
        r = positions.PositionClose(config.account_id, 'EUR_USD', {"shortUnits": "ALL"})
        resp = oanda.request(r)
        print resp
        pl = resp.get('shortOrderFillTransaction').get('tradesClosed')[0].get('realizedPL')
        real_profits.append(float(pl))
        print time, 's: Closed. Profit = ', pl, ' price = ', resp.get('shortOrderFillTransaction').get('price')
    except:
        print 'No short units to close'

def get_bal():
    r = AccountDetails(config.account_id)
    return oanda.request(r).get('account').get('balance')

plt.ion()
plt.grid(True)
do_close_long()
do_close_short()
real_profits = list()

while True:
    try:
        oanda.request(pReq)
        ask = float(pReq.response.get('prices')[0].get('asks')[0].get('price'))
        bid = float(pReq.response.get('prices')[0].get('bids')[0].get('price'))
        status = pReq.response.get('prices')[0].get('status')
        process_data(ask, bid, status)
        plt.clf()
        plt.subplot(1,2,1)
        plt.plot(times, asks, color='red', label='ASK')
        plt.plot(times, bids, color='blue', label='BID')
        if last_ask!=0:
            plt.axhline(last_ask, linestyle=':', color='red', label='curr ASK')
        if last_bid!=0:
            plt.axhline(last_bid, linestyle=':', color='blue', label='curr BID')
        plt.xlabel('Time, s')
        plt.ylabel('Price change')
        plt.legend(loc='upper left')
        plt.subplot(1, 2, 2)
        plt.hist(real_profits, label='Profits')
        plt.legend(loc='upper left')
        plt.xlabel('Profits')
        plt.ylabel('Counts')
        plt.tight_layout()

    except Exception as e:
        print e
    plt.pause(config.period)
    time = time + config.period


