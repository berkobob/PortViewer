""" Controller """

import os
import src.controller.constants as constants
from src.controller.ticker import Ticker

class Controller:

    def __init__(self, data):
        self.data = data
        self.portfolios = self.data.load()

    def load_portfolio(self, port):
        if port in self.portfolios.keys():
            print("Portfolio {} found".format(port))
        else:
            print("Creating portfolio", port)
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

        except IOError:
                return os.listdir(constants.DATAPATH)
        except Exception as e:
                text = ["Error report:"]
                text.append(str(e))
                return text

    def port_names(self):
        for name in self.portfolios.keys():
            yield name

    def valid_port(self, port):
        return port in self.portfolios.keys()

    def update(self, port):
        for ticker in self.portfolios[port]:
            ticker.updatePrice()
            yield ticker