from StockDataDownloader import StockDataDownloader as d
from datetime import date
import sklearn.model_selection as ms
import sklearn.preprocessing as pp
import sklearn.neighbors as neigh
import pandas

downloader = d.StockDataDownloader()
data = downloader.get_data_from_finam('SPFB.SI-9.16', 1, 17, 420658, date(2016,6,13), date(2016,9,12))
classes = list()
classes.append('No info')

print 'Preparing classes..'
for k in range(1,data.index.__len__()):
    if data['<CLOSE>'][k] > data['<CLOSE>'][k-1]:
        classes.append('Price grows')
    else:
         if data['<CLOSE>'][k] < data['<CLOSE>'][k - 1]:
             classes.append('Price falls')
         else:
             classes.append('No info')

print 'Scaling data..'

# ignore volume column
scaledData = pp.scale(data.take(range(2,6),axis=1))
kf = ms.KFold(n_splits=5,shuffle=True,random_state=42)

scores = list()
k_range = range(1,50)
for k in k_range:
    print 'Calculating scores for k=',k
    model = neigh.KNeighborsClassifier(n_neighbors=k)
    scs = ms.cross_val_score(model, scaledData, classes, cv=kf, scoring='accuracy')
    scores.append(scs)

results = pandas.DataFrame(scores, k_range).mean(axis=1).sort_values(ascending=False)

print 'Found best k=',results.head(1).index[0]