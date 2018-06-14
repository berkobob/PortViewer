import requests
from bs4 import BeautifulSoup
import src.controller.constants as constants

class Ticker(object):

    def __init__(self, data):
        self.ticker = data[0]
        self.shares = int(data[1])
        self.price = float(data[2])
        if data[3] == "LSE":
            self.__cleanName()
        self.last = 0.0
        self.delta = 0.0
        self.percent = 0.0
        self.stamp = "NO DATA"

    def to_dict(self):
        return {'ticker': self.ticker, 'shares': self.shares, 'price': self.price,
                'last': self.last, 'delta': self.delta, 'percent': self.percent}

    def __repr__(self):
        return "{} {:>6} is at £{:<10.2f} It's moved £{: 7.2f} which is {: 5.2f}%. We have {:5d} shares at £{: 6.2f} each".format(
            self.stamp, self.ticker, self.last, self.delta, self.percent, self.shares, self.price)

    def updatePrice(self):
        page = requests.get(constants.WWW+self.ticker)
        soup = BeautifulSoup(page.content, 'html.parser')

        price = soup.find('span', class_="Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)")
        if price:
            last = price.get_text()
            last = last.replace(',','')
            self.last = float(last)
        else:
            self.last = -1

        delta = soup.find('span', class_="Fw(500)")
        if delta:
            a, b = delta.get_text().split(' ')
            self.delta = float(a)
            self.percent = float(b.replace('(','').replace(')','').replace('%',''))
        else:
            self.delta, self.percent = 0, 0

        stamp = soup.find('div', attrs={'id': 'quote-market-notice' })
        if stamp:
            self.stamp = stamp.get_text().replace('  ',' ')
        else:
            self.stamp = "Error: could not update prices"


    def __cleanName(self):
        if self.ticker[-1] != '.':
            if '.' in self.ticker:
                self.ticker = self.ticker.replace('.','-')
            self.ticker = self.ticker+"."
        self.ticker = self.ticker+"L"

