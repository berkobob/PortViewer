class View:

    def __init__(self, controller):
        self.controller = controller

        print("Welcome to Portfolio Viewer, command line mode:")
        port = None

        while True: 
            print()
            print("Current portfolio", port)
            print("0 Quit")
            print("1 New portfolio")
            print("2 List portfolios")
            print("3 Update portfolio")
            print("4 View portfolio")
            print("5 Select portfolio")
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
                if port:
                    print("Getting prices. Please wait...")
                    for ticker in self.controller.update(port):
                        print(ticker)

            elif choice[0] == '4':
                if port:
                    for ticker in self.controller.get_port(port):
                        print (ticker)
                
            elif choice[0] == '5':
                ports = self.controller.port_names()
                for i in range(0, len(ports)):
                    print(i, ports[i])
                try:
                    port = ports[int(input("Which portfolio: "))]
                except:
                    print("Invalid selection. Selected portfolio is", port)


    def load_portfolio(self):
        file = input("File name: ")
        for text in self.controller.load_portfolio(file):
            print(text)
