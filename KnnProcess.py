from StockDataDownloader import StockDataDownloader as d
from datetime import date
from ClassifierTrainer import ClassifierTrainer

downloader = d.StockDataDownloader()

data = downloader.get_data_from_finam('SPFB.SI-9.16', 1, 17, 420658, date(2016,6,13), date(2016,9,12))
(model, K, acc) = ClassifierTrainer.train_classifier(data)
print "For SPFB.SI-9.16 best K=",K,'accuracy=',acc
