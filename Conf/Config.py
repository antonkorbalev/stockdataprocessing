import os
import os.path

class Config:
    def __init__(self):
        if not os.path.isdir('Account'):
            os.chdir('..')

        self.token = open('Account/Token.txt', 'r').read()
        self.env = 'practice'
        self.insName = 'EUR_USD'
        self.maxLength = 20 # ticks
        self.period = 1 # s
        self.write_back_log = False
        self.back_log_path = 'BackLog'
        self.account_id = open('Account/Account.txt', 'r').read()
        self.stop_loss_value = 0
        self.take_profit_value = 0
        self.lot_size = 10000

        # settings for candle analysis
        self.candlePeriod = 'M'  # period
        self.candleDiff = 15 # diff (in period value)
