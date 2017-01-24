from StockDataDownloader import StockDataDownloader as d
from datetime import date
from ClassifierTrainer import ClassifierTrainer
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import numpy
import pandas

def check_success(contractName, period, marketCode, em, indicies,compareIndex, train_date_start, train_date_stop, real_date_start, real_date_stop):
    downloader = d.StockDataDownloader()
    data = downloader.get_data_from_finam(contractName, period, marketCode, em, train_date_start, train_date_stop)
    ct = ClassifierTrainer()
    bestK = 0
    bestAcc = 0
    bestN = 0
    for nCandles in range(1,10):
        (K, acc) = ct.train_classifier(data, nCandles, indicies=indicies, compareIndex=compareIndex)
        if (K > 1) and (bestAcc < acc):
            bestK = K
            bestAcc = acc
            bestN = nCandles
        #print nCandles,': For SPFB.SI-6.16 best K=',K, 'accuracy=',acc
    print ' Best result = ', bestK, acc, ' [',bestN,']'
    ct.train_classifier(data, bestN, indicies=indicies, compareIndex=compareIndex)
    # processing data
    processData = downloader.get_data_from_finam(contractName, period, marketCode, em, real_date_start, real_date_stop).take(indicies, axis=1).as_matrix()
    ins = 0
    outs = 0
    for i in range(bestN, processData.__len__()-1,1):
        row = []
        for k in range(i-bestN, i,1):
            row = numpy.hstack((row, processData[k]))
        # compare model prediction with processData[i]
        predictVal = ct.predic_price_for_row([row])
        realVal = processData[i][compareIndex] > processData[i-1][compareIndex]
        # price grows
        if realVal == True:
            if predictVal == ['Buy']:
                ins = ins + 1
            else:
                outs = outs +1
        # price falls
        if realVal == False:
            if predictVal == ['Sell']:
                ins = ins + 1
            else:
                outs = outs +1

    return round(100 * float(ins) / float(ins+outs), 2)

indicies=[5,6]
#close index
compareIndex=0
period = 5

ddata = pandas.read_csv('Derivatives.dat').as_matrix()
ests = list()
for i in range(0, ddata.__len__()-1):
    contractName = ddata[i][0]
    em = ddata[i][1]
    marketCode = ddata[i][2]
    train_date_start = parse(ddata[i][3])
    real_date_stop = parse(ddata[i][4])
    train_date_stop = train_date_start + relativedelta(months=+1)
    real_date_start = train_date_stop + relativedelta(days=+1)
    print " Checking ", contractName
    success = check_success(contractName, period, marketCode, em, indicies,compareIndex, train_date_start, train_date_stop, real_date_start, real_date_stop)
    ests.append(success)
    print 'Success = ', success, '%'

print "Total model success = ", numpy.mean(ests)