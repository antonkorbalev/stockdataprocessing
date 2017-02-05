class Config:
    def __init__(self):
        self.token = open('Token.txt', 'r').read()
        self.insName = 'EUR_USD'
        self.maxLength = 100  # ticks
        self.period = 60  # s
        self.write_back_log = False
        self.back_log_path = 'BackLog'
        self.account_id = open('Account.txt', 'r').read()
        self.stop_loss_value = 0
        self.take_profit_value = 0
        # put orders when plus deals percent > percent_of_success
        self.percent_of_success = 50
        self.lot_size = 100
