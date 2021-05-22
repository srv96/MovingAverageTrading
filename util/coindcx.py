import hashlib
import hmac
import json
import time
import requests


class Api:
    @staticmethod
    def get_ticker():
        url = "https://api.coindcx.com/exchange/ticker"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_markets():
        url = "https://api.coindcx.com/exchange/v1/markets"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_markets_details():
        url = "https://api.coindcx.com/exchange/v1/markets_details"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_last_traded_price(pair):  # I-DOGE_INR
        url = "https://public.coindcx.com/market_data/trade_history?pair=" + pair + "&limit=1"
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_order_book(pair):
        url = "https://public.coindcx.com/market_data/orderbook?pair=" + pair
        response = requests.get(url)
        data = response.json()
        return data

    @staticmethod
    def get_candles(pair, time_frames, limit):
        url = "https://public.coindcx.com/market_data/candles?pair=" + pair + "&interval=" + time_frames + "&limit=" + limit
        response = requests.get(url)
        data = response.json()
        return data

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.secret_bytes = bytes(secret, encoding='utf-8')

    def get_user_info(self):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/users/info"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def get_balance(self, currency):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/users/balances"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        for d in data:
            if d['currency'] == currency:
                return d

    def buy_quantity_with_limit_order(self, market, price_per_unit, quantity):
        # secret_bytes = bytes(self.secret, encoding='utf-8')
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "buy",
            "order_type": "limit_order",
            "market": market,
            "price_per_unit": price_per_unit,
            "total_quantity": quantity,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/create"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def buy_fractional_with_limit_order(self, market, price_per_unit, amount):
        quantity = amount / price_per_unit
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "buy",
            "order_type": "limit_order",
            "market": market,
            "price_per_unit": price_per_unit,
            "total_quantity": quantity,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/create"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def sell_quantity_with_limit_order(self, market, price_per_unit, quantity):
        # secret_bytes = bytes(self.secret, encoding='utf-8')
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "sell",
            "order_type": "limit_order",
            "market": market,
            "price_per_unit": price_per_unit,
            "total_quantity": quantity,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/create"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def sell_fractional_with_limit_order(self, market, price_per_unit, amount):
        quantity = amount / price_per_unit
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "sell",
            "order_type": "limit_order",
            "market": market,
            "price_per_unit": price_per_unit,
            "total_quantity": quantity,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/create"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def get_order_status(self, order_id):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "id": order_id,  # Enter your Order ID here.
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/status"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def get_active_order(self, market):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "buy",
            "market": market,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/active_orders"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def get_trade_history(self, from_id, limits):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "from_id": from_id,
            "limit": limits,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(from_id.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/trade_history"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def get_active_order_count(self, market):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "buy",
            "market": market,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/active_orders_count"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def edit_price(self, deal_id, price_per_unit):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "id": deal_id,
            "timestamp": timeStamp,
            "price_per_unit": price_per_unit  # Enter the new-price here
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/edit"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def cancel(self, deal_id):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "ids": deal_id,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/cancel_by_ids"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def cancel_multiple_by_id(self, id_list):
        body = {
            "ids": id_list
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(id_list.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/cancel_by_ids"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data

    def cancel_all(self, market):
        timeStamp = int(round(time.time() * 1000))
        body = {
            "side": "buy",
            "market": market,
            "timestamp": timeStamp
        }
        json_body = json.dumps(body, separators=(',', ':'))
        signature = hmac.new(self.secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()
        url = "https://api.coindcx.com/exchange/v1/orders/cancel_all"
        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': self.key,
            'X-AUTH-SIGNATURE': signature
        }
        response = requests.post(url, data=json_body, headers=headers)
        data = response.json()
        return data
