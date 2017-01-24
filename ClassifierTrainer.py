import sklearn.model_selection as ms
import sklearn.preprocessing as pp
import sklearn.neighbors as neigh
import pandas
import numpy

class ClassifierTrainer(object):
    """ Contains methods for training classifiers """

    __model = neigh.KNeighborsClassifier()
    __nCandles = 0
    __indicies = range(2,6)
    __scale = False
    __compareIndex = 6

    def predic_price_for_row(self, row):
        return self.__model.predict(row)

    # predicts price for last used parameters
    def predict_price_for_data(self, data):
        data = data.take(self.__indicies, axis=1)
        if self.__scale:
            data = pp.scale(data)
        # get row for prediction
        data = data.tail(self.__nCandles).as_matrix()
        row = []
        for i in range(0, data.__len__()):
            row = numpy.hstack((row, data[i]))
        return self.__model.predict([row])

    def get_patterns(self, data, nCandles, scale, indicies, compareIndex):
        """ Generates patterns for n candles
            Data - data to process
            nCandles - N candles in a template
            scale - scale or not
            indicies - what columns to consider
            compareIndex - decision column index (sell or by, often <CLOSE> column)
        """
        classes = list()
        rows = list()
        data = data.take(indicies, axis=1).as_matrix()
        if scale:
            data = pp.scale(data)
        for i in range(nCandles,data.__len__()-2):
            # take N candles and split into line (dimension reduction)
            row = []
            for i in range(i-nCandles,i):
                row = numpy.hstack((row, data[i]))
            rows.append(row)
            # get class for pattern
            if data[i][compareIndex] < data[i+1][compareIndex]:
                classes.append('Buy')
            else:
                classes.append('Sell')
        return (rows, classes)

    def train_classifier(self, data, nCandles, scale = False, indicies = range(2,6), compareIndex = 3):
        """ Trains classifier and returns model, best K and accuracy """
        self.__compareIndex = compareIndex
        self.__indicies = indicies
        self.__scale = False
        self.__nCandles = nCandles
        (dataToProcess, classes) = self.get_patterns(data, nCandles, scale, indicies, compareIndex )
        kf = ms.KFold(n_splits=5, shuffle=True, random_state=42)
        scores = list()
        k_range = range(1, 50)
        for k in k_range:
            model = neigh.KNeighborsClassifier(n_neighbors=k)
            scs = ms.cross_val_score(model, dataToProcess, classes, cv=kf, scoring='accuracy')
            scores.append(scs)

        results = pandas.DataFrame(scores, k_range).mean(axis=1).sort_values(ascending=False)
        #train model on best K
        bestK = results.head(1).index[0]
        acc = results.head(1).values[0]
        self.__model = neigh.KNeighborsClassifier(n_neighbors=bestK)
        self.__model.fit(dataToProcess, classes)
        return bestK, acc