from StockDataDownloader import StockDataDownloader as d
from datetime import date
from ClassifierTrainer import ClassifierTrainer

downloader = d.StockDataDownloader()

data = downloader.get_data_from_finam('SPFB.SI-6.16', 5, 17, 414253, date(2016,3,11), date(2016,6,12))
ct = ClassifierTrainer()
for nCandles in range(1,10):
    (K, acc) = ct.train_classifier(data, nCandles, indicies=[5], compareIndex=0)
    print ct.predict_price(data)
    print nCandles,': For SPFB.SI-6.16 best K=',K, 'accuracy=',acc

