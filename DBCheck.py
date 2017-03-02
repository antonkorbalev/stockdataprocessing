import psycopg2
from Conf import DbConfig, Config
from datetime import datetime, timedelta

def CheckDB_for_period(periodInSeconds):
    conf = Config.Config()
    dbConf = DbConfig.DbConfig()
    connect = psycopg2.connect(database=dbConf.dbname, user=dbConf.user, host=dbConf.address, password=dbConf.password)
    cursor = connect.cursor()

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
            if delta != timedelta(seconds=periodInSeconds):
                print 'Error: difference in time is ', delta
                break
        lastTimeStamp = timeStamp
    return error

error = CheckDB_for_period(5)
if not error:
    print "Database is OK."


