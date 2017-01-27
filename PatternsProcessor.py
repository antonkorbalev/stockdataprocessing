import sklearn.preprocessing as pp
import numpy

class PatternProcessor(object):
    """ Contains methods for processing patterns """

    def get_patterns(self, data, nCandles, indicies, compareIndex):
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