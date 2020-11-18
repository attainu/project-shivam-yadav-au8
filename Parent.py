class BitcoinParent:
    def __init__(self,val,thr):
        self.val=val #foe eg BTC ,ETH etc
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol='+self.val+'&convert=USD'
        self.headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'deflate, gzip',
            'X-CMC_PRO_API_KEY': '398f748f-8cdc-4eec-85c7-2a2b6da5efeb',
        }
        self.BITCOIN_PRICE_THRESHOLD = thr #threshold value
        self.IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/ivOYKfsEfFdFRplLrL6Q2HFbOiS85Mn8vTinPaBe2tO'
