import sklearn.model_selection as ms
import sklearn.preprocessing as pp
import sklearn.neighbors as neigh
import pandas

class ClassifierTrainer(object):
    """ Contains methods for training classifiers """
    @staticmethod
    def train_classifier(data):
        """ Trains classifier and returns model, best K and accuracy """
        classes = list()
        classes.append('No info')

        for k in range(1, data.index.__len__()):
            if data['<CLOSE>'][k] > data['<CLOSE>'][k - 1]:
                classes.append('Price grows')
            else:
                if data['<CLOSE>'][k] < data['<CLOSE>'][k - 1]:
                    classes.append('Price falls')
                else:
                    classes.append('No info')

        # ignore volume column
        scaledData = pp.scale(data.take(range(2, 6), axis=1))
        kf = ms.KFold(n_splits=5, shuffle=True, random_state=42)

        scores = list()
        k_range = range(1, 50)
        for k in k_range:
            model = neigh.KNeighborsClassifier(n_neighbors=k)
            scs = ms.cross_val_score(model, scaledData, classes, cv=kf, scoring='accuracy')
            scores.append(scs)

        results = pandas.DataFrame(scores, k_range).mean(axis=1).sort_values(ascending=False)
        return model, results.head(1).index[0], results.head(1).values[0]