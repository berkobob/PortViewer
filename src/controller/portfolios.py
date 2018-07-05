""" Controller """

import os
import src.controller.constants as constants
from src.controller.ticker import Ticker

class Controller:

    def __init__(self, data):
        self.data = data
        self.portfolios = self.data.load()

    def load_portfolio(self, port, filetoload):

        self.portfolios[port] = []

        #path = constants.DATAPATH+port+'.csv'
        try:
            with open(filetoload) as file:
                file.readline()
                row=file.readline().rstrip('\n').split(',')

                while len(row) > 1:
                    self.portfolios[port].append(Ticker(row))
                    row=file.readline().rstrip('\n').split(',')

                self.data.save(self.portfolios)
                return self.portfolios[port]

        except Exception as e:
                text = ["Error report:"]
                text.append(str(e))
                return text

    def port_names(self):
        return list(self.portfolios.keys())

    def valid_port(self, port):
        return port in self.portfolios.keys()

    def realtime_update(self, port):
        for ticker in self.portfolios[port]:
            ticker.updatePrice()
            yield ticker
        self.data.save(self.portfolios)

    def update(self, port):
        for ticker in self.portfolios[port]:
            ticker.updatePrice()
        self.data.save(self.portfolios)

    def get_port(self, port):
        return self.portfolios[port]

    def delete(self, port):
        del self.portfolios[port]
        self.data.save(self.portfolios)

    def sort(self, port, col, asc):
        if col == "name":
            self.portfolios[port].sort(key=lambda x: x.name, reverse=asc)
        elif col == "shares":
            self.portfolios[port].sort(key=lambda x: x.shares, reverse=asc)
        elif col == "price":
            self.portfolios[port].sort(key=lambda x: x.price, reverse=asc)
        elif col == "last":
            self.portfolios[port].sort(key=lambda x: x.last, reverse=asc)
        elif col == "delta":
            self.portfolios[port].sort(key=lambda x: x.delta, reverse=asc)
        elif col == "percent":
            self.portfolios[port].sort(key=lambda x: x.percent, reverse=asc)

        return self.portfolios[port]

    def new_port(self, port):
        self.portfolios[port] = []
        self.data.save(self.portfolios)

    def add_ticker(self, port, data):
        self.portfolios[port].append(Ticker(data))
        self.data.save(self.portfolios)

    def del_ticker(self, port, ticker):
        self.portfolios[port] = [x for x in self.portfolios[port] if x.to_dict()['ticker'] != ticker]
        self.data.save(self.portfolios)