from StockDataDownloader import StockDataDownloader
from datetime import date
import unittest


class DownloaderTests(unittest.TestCase):
    """Test methods for StockDataDownloader"""

    def test_downloader(self):
        downloader = StockDataDownloader()
        data = downloader.get_data_from_finam('SPFB.SI-9.16', 5, 17, 420658, date(2016,6,13), date(2016,9,12))
        self.assertTrue(data.__len__() == 910, 'Invalid number of rows!')
        self.assertTrue(data.shape[1] == 7, 'Invalid number of columns!')

if __name__ == '__main__':
    unittest.main()
