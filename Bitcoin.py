import pandas as pd
import numpy as np
import time
import requests
import json
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
class BitcoinParent:
    def __init__(self,val,thr):
        self.val=val
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='+self.val+'&convert=USD'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'deflate, gzip',
            'X-CMC_PRO_API_KEY': '398f748f-8cdc-4eec-85c7-2a2b6da5efeb',
        }
        self.BITCOIN_PRICE_THRESHOLD = thr
        self.IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/ivOYKfsEfFdFRplLrL6Q2HFbOiS85Mn8vTinPaBe2tO'

class Bitcoin(BitcoinParent):
    def __init__(self,val,thr):
        super().__init__(val,thr)
    def get_latest_bitcoin_price(self):
        # print(self.val)
        response = requests.get(self.url, headers=self.headers)
        response_json = response.json()
        # time.sleep(0.07* 60) 
        # print(response_json)
        return (response_json['data'][self.val]['quote']['USD']['price'])
    def post_ifttt_webhook(self,event, value):
        data = {'value1': value}
        ifttt_event_url = self.IFTTT_WEBHOOKS_URL.format(event)
        requests.post(ifttt_event_url, json=data)
    def format_bitcoin_history(self,bitcoin_history):
        rows = []
        for bitcoin_price in bitcoin_history:
            date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
            price = bitcoin_price['price']
            row = '{}: $<b>{}</b>'.format(date, price)
            rows.append(row)
        return '<br>'.join(rows)


    def main(self):
        bitcoin_history = []
        x1=[]
        y1=[]
        p=[]
        d=[]
        while True:
            price =self.get_latest_bitcoin_price()
            date = datetime.now()
            bitcoin_history.append({'date': date, 'price': price})
            a,b=(str(date)).split()
            ddate=a
            d.append(b)
            p.append(price)
            if(len(bitcoin_history) <= 15):
                x1.append([price])
            print(date, "$", price)
            if price < self.BITCOIN_PRICE_THRESHOLD:
                self.post_ifttt_webhook('bitcoin_price_emergency', price)
            if len(bitcoin_history) == 5:
                self.post_ifttt_webhook('bitcoin_price_update',self.format_bitcoin_history(bitcoin_history[-5:]))
                # bitcoin_history = []
            if(len(bitcoin_history) > 15):
                y1.append(price)
            if(len(bitcoin_history)==30):
                x= np.array(x1)
                y= np.array(y1)
                x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
                svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.00001)
                svr_rbf.fit(x_train, y_train)
                svr_rbf_confidence = svr_rbf.score(x_test, y_test)
                print("accuracy: ", svr_rbf_confidence)
                svm_prediction = svr_rbf.predict(x_test)
                print(svm_prediction)
                print(sum(svm_prediction)/len(svm_prediction))
                with plt.style.context('dark_background'):
                    plt.plot(d, p, color='blue', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='red', markersize=12)  
                    plt.plot(d[-len(svm_prediction):],svm_prediction, color='cyan', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='green', markersize=12)  
                    plt.legend('Price vs Date', ncol=2, loc='upper left')
                    plt.ylabel('Price')
                    plt.xlabel(ddate)
                    plt.show()
                break
            if(len(p)%15==0):
                with plt.style.context('dark_background'):
                    plt.plot(d, p, color='blue', linestyle='dashed', linewidth = 3,marker='o', markerfacecolor='red', markersize=12) 
                    plt.legend('Price vs Date', ncol=2, loc='upper left')
                    plt.ylabel('Price')
                    plt.xlabel(ddate)
                    plt.show()
val=input('''Type :
BTC: Bitcoin  
ETH: Ethereum 
XRP: XRP 
LTC: Litecoin
BCH: Bitcoin Cash
BNB: Binance Coin
DOT: Polkadot 
ADA: Cardano
BSV: Bitcoin SV
EOS:Eos 
''')
thr=int(input('''Enter the threshold :'''))
obj=Bitcoin(val,thr)
obj.main()
