from StockDataDownloader import StockDataDownloader as d
from datetime import date
from ClassifierTrainer import ClassifierTrainer
import sklearn.preprocessing as pp

downloader = d.StockDataDownloader()

data = downloader.get_data_from_finam('SPFB.SI-6.16', 1, 17, 414253, date(2016,3,11), date(2016,6,12))
(model, K, acc) = ClassifierTrainer.train_classifier(data)
print 'For SPFB.SI-6.16 best K=',K, 'accuracy=',acc

