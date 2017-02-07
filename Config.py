class Config:
    def __init__(self):
        self.token = open('Token.txt', 'r').read()
        self.insName = 'EUR_USD'
        self.maxLength = 50 # ticks
        self.period = 1 # s
        self.write_back_log = False
        self.back_log_path = 'BackLog'
        self.account_id = open('Account.txt', 'r').read()
        self.stop_loss_value = 0
        self.take_profit_value = 0
        self.lot_size = 10000
        self.max_pos_time = 3600*6 #s
