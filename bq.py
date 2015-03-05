#!/usr/bin/python
"""
Real time bitcoin rate exchange.
It shows BTC exchange rates in USD and EUR.
With optional argument (BTC amount), also shows equivalent values in USD and EUR.
Examples:
./bq.py
./bq.py 0.00272223
Many thanks to http://blockr.io and http://rate-exchange.appspot.com !
Author: Fabio Pani (@fabiux): http://www.fabiopani.it
"""
from sys import argv
from urllib2 import Request, build_opener
from json import loads

EUR_USD_URL = 'http://rate-exchange.appspot.com/currency?from=USD&to=EUR'
BQ_URL = "http://btc.blockr.io/api/v1/coin/info"
URLTIMEOUT = 30


def get_url(url):
    try:
        request = Request(url)
        opener = build_opener()
        respdata = opener.open(request, timeout=URLTIMEOUT)
        if respdata.code == 200:
            return respdata.read()
        else:
            return None
    except:
        return None


def main():
    if len(argv) == 1:
        btc = 1.0
    else:
        btc = float(argv[1])
    eurdollar = get_url(EUR_USD_URL)
    if eurdollar is None:
        eur_rate = 0.0
    else:
        j = loads(eurdollar)
        eur_rate = j['rate']
    bq = get_url(BQ_URL)
    if bq is None:
        print("Error reading bitcoin quotations")
    else:
        j = loads(bq)
        value = j['data']['markets']['coinbase']['value']
        print("1 BTC = %s USD (%s EUR)" % (str(round(value, 2)), str(round(value * eur_rate, 2))))
        if btc != 1.0:
            print("%s BTC = %s USD (%s EUR)" % (str(btc), str(round(btc * value, 2)),
                  str(round(btc * value * eur_rate, 2))))

if __name__ == '__main__':
    main()