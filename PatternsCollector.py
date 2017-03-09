import psycopg2
from Conf import DbConfig, Config
from Desc.Candle import Candle
from Desc.Pattern import Pattern
import numpy

def get_patterns_for_window_and_num(window, length, limit=None):
    conf = Config.Config()
    dbConf = DbConfig.DbConfig()
    connect = psycopg2.connect(database=dbConf.dbname, user=dbConf.user, host=dbConf.address, password=dbConf.password)
    cursor = connect.cursor()

    print 'Successfully connected'
    tName = conf.insName.lower()
    cmd = 'SELECT COUNT(*) FROM {0};'.format(tName)
    cursor.execute(cmd)
    totalCount = cursor.fetchone()[0]
    print 'Total items count {0}'.format(totalCount)
    cmd = 'SELECT * FROM {0} ORDER BY datetimestamp'.format(tName)
    if limit is None:
        cmd = '{0};'.format(cmd)
    else:
        cmd = '{0} LIMIT {1};'.format(cmd, limit)
    cursor.execute(cmd)

    wl = list()
    patterns = list()
    profits = list()
    indicies = list()
    i = 1
    for row in cursor:
        nextCandle = Candle(row[0], row[1], row[2], row[3])
        wl.append(nextCandle)
        print 'Row {0} of {1}, {2:.3f}% total'.format(i, totalCount, 100*(float(i)/float(totalCount)))
        if len(wl) == window+length:
            # find pattern of 0..length elements
            # that indicates price falls / grows
            # in the next windows elements to get profit
            candle = wl[length-1]
            ind = length + 1
            # take real data only
            if candle.volume != 0:
                while ind <= window + length:
                    iCandle = wl[ind-1]
                    # define patterns for analyzing iCandle
                    if iCandle.volume != 0:
                        if iCandle.bid > candle.ask:
                            # buy pattern
                            p = Pattern(wl[:length],'buy')
                            patterns.append(p)
                            indicies.append(ind - length)
                            profits.append(iCandle.bid - candle.ask)
                            break
                        if iCandle.ask < candle.bid:
                            # buy pattern
                            p = Pattern(wl[:length],'sell')
                            patterns.append(p)
                            indicies.append(ind - length)
                            profits.append(candle.bid - iCandle.ask)
                            break
                    ind = ind + 1
            wl.pop(0)
        i = i + 1
    print 'Total patterns: {0}'.format(len(patterns))
    print 'Mean index[after]: {0}'.format(numpy.mean(indicies))
    print 'Mean profit: {0}'.format(numpy.mean(profits))
    connect.close()
    return patterns


def pattern_serie_to_vector(pattern):
    vec = []
    for candle in pattern.serie:
        vec = numpy.hstack((vec, [candle.ask, candle.bid, candle.volume]))
    return vec


def get_x_y_for_patterns(patterns):
    X = []
    y = []
    for p in patterns:
        X.append(pattern_serie_to_vector(p))
        y.append(p.result)
    return X, y
