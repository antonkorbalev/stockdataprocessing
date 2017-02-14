import psycopg2
from StockDataDownloader import StockDataDownloader
from Conf import DbConfig, Config
from datetime import datetime, timedelta
import oandapyV20
import re

step = 6 # hrs
dbConf = DbConfig.DbConfig()
conf = Config.Config()
connect = psycopg2.connect(database=dbConf.dbname, user=dbConf.user, host=dbConf.address, password=dbConf.password)
cursor = connect.cursor()

print 'Successfully connected'
cursor.execute("SELECT * FROM pg_tables WHERE schemaname='public';")
tables = list()
for row in cursor:
    tables.append(row[1])
for name in tables:
    cmd = "DROP TABLE "+name
    print cmd
    cursor.execute(cmd)
connect.commit()

cmd = ('CREATE TABLE public."{0}" (' \
    '"DateTimeStamp" TIMESTAMP WITHOUT TIME ZONE NOT NULL,' \
    '"Ask" FLOAT NOT NULL,' \
    '"Bid" FLOAT NOT NULL,' \
    '"Volume" FLOAT NOT NULL,' \
    'CONSTRAINT "PK_ID" PRIMARY KEY ("DateTimeStamp"));' \
    'CREATE UNIQUE INDEX timestamp_idx ON {0} ("DateTimeStamp");').format(dbConf.tablename)
cursor.execute(cmd)
connect.commit()

print 'Created table',dbConf.tablename

daysTotal = 100 #int(raw_input('Days to import: '))
insName = 'EUR_USD' #raw_input('Specify instrument name: ')
timeFrame = 'S5' #raw_input('Time frame: ')

downloader = StockDataDownloader.StockDataDownloader()
oanda = oandapyV20.API(environment=conf.env, access_token=conf.token)

def parse_date(dt):
    broken = re.search(r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})(\.([0-9]+))?(Z|([+-][0-9]{2}):([0-9]{2}))', dt)
    return(datetime(
        year = int(broken.group(1)),
        month = int(broken.group(2)),
        day = int(broken.group(3)),
        hour = int(broken.group(4)),
        minute = int(broken.group(5)),
        second = int(broken.group(6)),
        microsecond = int(broken.group(8) or "0")))

date = datetime.utcnow() - timedelta(days=daysTotal)
dateStop = datetime.utcnow()

last_id = ''
while date < dateStop:
    dateFrom = date
    dateTo = date + timedelta(hours=step)
    data = downloader.get_data_from_oanda_fx(oanda, insName, timeFrame,
       dateFrom, dateTo)
    if len(data.get('candles')) > 0:
        cmd = ''
        cmd = 'INSERT INTO stockdata VALUES'
        cmd_bulk = ''
        for candle in data.get('candles'):
            id = parse_date(candle.get('time'))
            if last_id!=id:
                cmd_bulk = cmd_bulk + ("(TIMESTAMP '{0}',{1},{2},{3}),\n"
                    .format(id,candle.get('ask')['c'], candle.get('bid')['c'],candle.get('volume')))
            else:
                print 'Double id ',id,' skipped.'
            last_id = id
        cmd = cmd + cmd_bulk[:-2] + ';'
        cursor.execute(cmd)
        connect.commit()
    print ("Saved candles from {0} to {1}".format(dateFrom, dateTo))
    date = dateTo

cmd = "REINDEX INDEX timestamp_idx;"
print cmd
cursor.execute(cmd)
connect.commit()

connect.close()

