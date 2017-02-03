from __future__ import absolute_import
from StockDataDownloader import StockDataDownloader
from PatternsProcessor import PatternProcessor
from datetime import date
import unittest
import pandas
import numpy
import oandapy


class DownloaderTests(unittest.TestCase):
    """Test methods for StockDataDownloader"""

    def test_downloader(self):
        downloader = StockDataDownloader.StockDataDownloader()
        data = downloader.get_data_from_finam('SPFB.SI-9.16', 5, 17, 420658, date(2016,6,13), date(2016,9,12))
        self.assertTrue(data.__len__() == 910, 'Invalid number of rows!')
        self.assertTrue(data.shape[1] == 7, 'Invalid number of columns!')

    def test_patterns(self):
        proc = PatternProcessor()
        downloader = StockDataDownloader.StockDataDownloader()
        data = downloader.get_data_from_finam('SPFB.SI-9.16', 5, 17, 420658, date(2016, 6, 13), date(2016, 9, 12))
        (rows, classes) = proc.get_patterns(data,5, range(2,6),3)
        self.assertTrue(rows.__len__() == classes.__len__())
        data = pandas.DataFrame([[0,0,1,2,3,4,0],[0,0,5,6,7,8,0], [0,0,9,10,11,12,0], [0,0,1,2,3,4,0],[0,0,5,6,7,8,0], [0,0,9,10,11,12,0]])
        (rows, classes) = proc.get_patterns(data,2,range(2,6),3)
        self.assertTrue(classes == ['Buy', 'Sell'])
        self.assertTrue(numpy.allclose(rows,[[1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 7, 8, 9, 10, 11, 12]]))

    def test_accounts(self):
        token = open('../Token.txt', 'r').read()
        oanda = oandapy.API(environment="practice", access_token=token)
        accs = oanda.get_accounts().get('accounts')
        self.assertTrue(len(accs) > 0)

if __name__ == '__main__':
    unittest.main()
