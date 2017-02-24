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
        print timeStamp
        if lastTimeStamp!=datetime.min:
            delta = timeStamp - lastTimeStamp
            if delta != timedelta(seconds=periodInSeconds):
                # if same day
                if delta.days == 0:
                    print 'Error: difference in time is ', delta
                    error = True
                    break
        lastTimeStamp = timeStamp
    return error

error = CheckDB_for_period(60*50)
if not error:
    print "Database is OK."


