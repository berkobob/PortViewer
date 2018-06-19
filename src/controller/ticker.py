import requests
from bs4 import BeautifulSoup
import controller.constants as constants
import re

class Ticker(object):

    def __init__(self, data):
        self.name = data[0]
        self.ticker = data[0]
        self.shares = int(data[1])
        self.price = float(data[2])
        self.exchange = data[3]
        self.last = 0.0
        self.delta = 0.0
        self.percent = 0.0
        self.stamp = "NO DATA"
        self.symbol = '$'
        if self.exchange == "LSE":
            self.__cleanName()
            self.symbol = '£'


    def to_dict(self):
        #temp fix
        #self.symbol = "&"

        try:
            get_time = re.compile("\d{1,2}:\d{2}[A-Z]{2}\s[A-Z]{3}") #re.compile("\d{1,2}:\d{2}(AM|PM) [\w]")
            time_stamp = get_time.findall(self.stamp)[0]
        except Exception as e:
            time_stamp = "UPDATE"

        return {'ticker': self.name, 
                'shares': "{:0,}".format(self.shares), 
                'price': self.symbol+"{:.2f}".format(self.price),
                'last': self.symbol+"{:0,.2f}".format(self.last), 
                'delta': self.symbol+"{:0,.2f}".format(self.delta), 
                'percent': "{:0,.2f}%".format(self.percent), 
                'stamp': time_stamp
                }

    def __repr__(self):
        return "{} {:>6} is at {}{:<10.2f} It's moved {: 7.2f} which is {: 5.2f}%. We have {:5d} shares at {: 6.2f} each {} {}".format(
            self.stamp, self.name, self.symbol, self.last, self.delta, self.percent, self.shares, self.price, self.ticker, self.exchange)

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

