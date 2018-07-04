import pickle

class Data:
    """
    1. Load portfolios
    2. Save portfolios
    """
    def __init__(self):
        pass

    def save(self, data):
        with open('data.dat', 'wb') as file:
            pickle.dump(data, file) 

    def load(self):
        try:
            with open('data.dat', 'rb') as file:
                return pickle.load(file)
        except Exception as e:
            return {}
