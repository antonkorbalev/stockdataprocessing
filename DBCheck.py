import psycopg2
from Conf import DbConfig, Config
from datetime import datetime, timedelta

def checkDB_for_period():
    conf = Config.Config()
    dbConf = DbConfig.DbConfig()
    connect = psycopg2.connect(database=dbConf.dbname, user=dbConf.user, host=dbConf.address, password=dbConf.password)
    cursor = connect.cursor()
    cursor.itersize = 1000

    candleDiff = conf.candleDiff
    if conf.candlePeriod == 'M':
        candleDiff = candleDiff * 60
    if conf.candlePeriod == 'H':
        candleDiff = candleDiff * 3600

    print 'Successfully connected'
    tName = conf.insName.lower()

    cmd = 'SELECT * FROM {0} ORDER BY datetimestamp;'.format(tName)
    cursor.execute(cmd)

    lastTimeStamp = datetime.min
    error = False
    for row in cursor:
        timeStamp = row[0]
        if lastTimeStamp!=datetime.min:
            delta = timeStamp - lastTimeStamp
            if delta != timedelta(seconds=candleDiff):
                print 'Error: difference in time is ', delta
                break
        lastTimeStamp = timeStamp

    connect.close()
    return error

error = checkDB_for_period()
if not error:
    print "Database is OK."


