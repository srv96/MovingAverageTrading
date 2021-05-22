from datetime import datetime

import numpy as np
import time
from util.coindcx import Api


class TradingBot:

    def __init__(self, key, secret, pair, currency, time_frame, long_window, short_window, market,
                 quantity):
        self.key = key
        self.secret = secret
        self.market = market
        self.pair = pair
        self.currency = currency
        self.time_frame = time_frame
        self.long_window = long_window
        self.short_window = short_window
        self.quantity = quantity
        self.bought = False
        self.close = []
        self.short_avg = 0
        self.long_avg = 0
        self.api = Api(self.key, self.secret)
        self.file = float("nan")
        self.timestamp = 0

    @property
    def current_long_avg(self):
        return np.mean(self.close)

    @property
    def current_short_avg(self):
        return np.mean(self.close[:self.short_window])

    def take_decision(self):
        if self.short_avg > self.long_avg:
            if self.bought:
                return "DO NOTHING"
            else:
                self.bought = True
                return "BUY"
        else:
            if self.bought:
                self.bought = False
                return "SELL"
            else:
                return "DO NOTHING"

    def update_queue(self):
        self.close = []
        response = Api.get_candles(self.pair, self.time_frame, str(self.long_window))
        self.timestamp = int(response[0]['time']) / 1000
        for i in range(self.long_window):
            self.close.append(response[i]['close'])
        self.short_avg = self.current_short_avg
        self.long_avg = self.current_long_avg

    def log_writer(self, price, side):
        self.file = open('./log/logger.txt', 'a')
        self.file.write(
            datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S') + "," + str(self.close[0]) + "," + str(
                self.short_avg) + "," + str(self.long_avg) + "," + str(self.pair) + "," + str(self.market)+"," + str(
                self.quantity) + "," + str(price) + "," + side + "\n")
        self.file.close()

    def trade(self):
        self.update_queue()
        decision = self.take_decision()
        if decision == "BUY":
            price = Api.get_last_traded_price(self.pair)[0]['p']
            self.api.buy_quantity_with_limit_order(self.market, price, self.quantity)
            self.log_writer("price", "BOUGHT")
            pass
        elif decision == "SELL":
            price = Api.get_last_traded_price(self.pair)[0]['p']
            self.api.sell_quantity_with_limit_order(self.market, price, self.quantity)
            self.log_writer("price", "SOLD")
            pass
        else:
            self.log_writer("price", "IDLE")
            pass


bot = TradingBot(key="",
                 secret="",
                 pair="I-ETH_INR",
                 market="ETHINR",
                 currency="INR",
                 time_frame="1m",
                 long_window=25,
                 short_window=10,
                 quantity=0.001
                 )

while True:
    bot.trade()
    time.sleep(15)
