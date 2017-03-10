from __future__ import absolute_import
from StockDataDownloader import StockDataDownloader
from PatternsCollector import Pattern, Candle, pattern_serie_to_vector, get_x_y_for_patterns
from datetime import date, datetime, timedelta
import unittest
import pandas
import numpy
import oandapyV20
from oandapyV20.endpoints.accounts import AccountList, AccountDetails
from oandapyV20.endpoints.pricing import PricingInfo
from oandapyV20.contrib.requests import MarketOrderRequest
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.positions as positions

class GeneralTests(unittest.TestCase):
    """Test methods for StockDataDownloader"""

    def test_downloader(self):
        downloader = StockDataDownloader.StockDataDownloader()
        data = downloader.get_data_from_finam('SPFB.SI-9.16', 5, 17, 420658, date(2016,6,13), date(2016,9,12))
        self.assertTrue(data.__len__() == 910, 'Invalid number of rows!')
        self.assertTrue(data.shape[1] == 7, 'Invalid number of columns!')

    def test_accounts(self):
        token = open('../Account/Token.txt', 'r').read()
        accId = open('../Account/Account.txt', 'r').read()
        oanda = oandapyV20.API(environment="practice", access_token=token)
        r = AccountList()
        oanda.request(r)
        accsInfo = r.response.get('accounts')
        self.assertTrue(len(accsInfo) > 0)
        p = PricingInfo(accId, "instruments=EUR_USD")
        oanda.request(p)
        print p.response
        self.assertTrue(len(p.response.get('prices')) > 0)

    # for demo accounts only!
    def test_market_orders(self):
        token = open('../Account/Token.txt', 'r').read()
        accId = open('../Account/Account.txt', 'r').read()
        oanda = oandapyV20.API(environment="practice", access_token=token)
        mktOrder = MarketOrderRequest(instrument='EUR_USD',units=1)
        r = orders.OrderCreate(accId, data=mktOrder.data)
        resp = oanda.request(r)
        print resp
        r = positions.PositionClose(accId, 'EUR_USD',{"longUnits": "ALL"})
        resp = oanda.request(r)
        print resp
        r = AccountDetails(accId)
        balance = oanda.request(r).get('account').get('balance')
        self.assertTrue(balance > 0)

    # do not forget UTC now!
    def test_oanda_fx_history(self):
        token = open('../Account/Token.txt', 'r').read()
        oanda = oandapyV20.API(environment="practice", access_token=token)
        downloader = StockDataDownloader.StockDataDownloader()
        dateFrom = datetime.utcnow() - timedelta(days=1)
        dateTo = datetime.utcnow()
        result = downloader.get_data_from_oanda_fx(oanda, 'EUR_USD','S5',
                dateFrom, dateTo)
        self.assertTrue(len(result) > 0)

    def test_pattern_serie_to_vector(self):
        c1 = Candle(datetime.now(),1, 2, 3)
        c2 = Candle(datetime.now(), 4, 5, 6)
        p = Pattern([c1,c2],'test')
        self.assertTrue(numpy.allclose(pattern_serie_to_vector(p), [1,2,3,4,5,6]))

    def test_get_x_y_for_patterns(self):
        c1 = Candle(datetime.now(), 1, 2, 3)
        c2 = Candle(datetime.now(), 4, 5, 6)
        p = Pattern([c1,c2],'test1')
        c3 = Candle(datetime.now(), 7, 8, 9)
        c4 = Candle(datetime.now(), 10, 11, 12)
        p1 = Pattern([c3,c4],'test2')
        X, y = get_x_y_for_patterns([p, p1],'test2')
        self.assertEqual(y, [0,1])
        self.assertTrue(numpy.allclose(X[0], [1, 2, 3, 4, 5, 6]))
        self.assertTrue(numpy.allclose(X[1], [7, 8, 9, 10, 11, 12]))

if __name__ == '__main__':
    unittest.main()
