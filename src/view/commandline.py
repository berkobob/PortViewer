class View:

    def __init__(self, controller):
        self.controller = controller

        print("Welcome to Portfolio Viewer, command line mode:")

        while True: 
            print()
            print("0 Quit")
            print("1 New portfolio")
            print("2 List portfolios")
            print("3 View portfolio")
            choice = input(": ")
        
            if choice[0] == '0':
                print("Bye!")
                break

            elif choice[0] == '1':
                print("OK, loading new portfolio")
                self.load_portfolio()

            elif choice[0] == '2':
                print("Listing portfolios:")
                for port in self.controller.port_names():
                    print(port)

            elif choice[0] == '3':
                port = input("Which portfolio:")
                if self.controller.valid_port(port):
                    self.update(port)
                else:
                    print("Portfolio", port, "not found")

    def update(self, port):
        print("Getting prices. Please wait...")
        for ticker in self.controller.update(port):
            print(ticker)

    def load_portfolio(self):
        file = input("File name: ")
        results = self.controller.load_portfolio(file)
        
        for text in results:
            print(text)

        i = input("Porfolio {} loaded. Update prices (y/n)? ".format(file))
        if i.lower() == "y":
            self.update(file)



