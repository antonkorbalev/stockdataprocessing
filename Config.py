class Config:
    def __init__(self):
        self.token = open('Token.txt', 'r').read()
        self.insName = 'EUR_USD'
        self.maxLength = 100  # ticks
        self.period = 1  # s
        self.write_back_log = True
        self.back_log_path = 'BackLog'
