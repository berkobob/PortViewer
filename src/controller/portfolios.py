""" Controller """

import os
import controller.constants as constants
from .ticker import Ticker

class Controller:

    def __init__(self, data):
        self.data = data
        self.portfolios = self.data.load()

    def load_portfolio(self, port):

        self.portfolios[port] = []

        path = constants.DATAPATH+port+'.csv'
        try:
            with open(path) as file:
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
