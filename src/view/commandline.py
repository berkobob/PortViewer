import os

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
            print("6 Delete portfolio")
            choice = input(": ")
        
            if choice[0] == '0':
                print("Bye!")
                break

            elif choice[0] == '1':
                self.load_portfolio()

            elif choice[0] == '2':
                for port_name in self.controller.port_names():
                    print(port_name)

            elif choice[0] == '3':
                if port:
                    print("Getting prices. Please wait...")
                    for ticker in self.controller.realtime_update(port):
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

            elif choice[0] == '6':
                if port:
                    if input("Enter YES to confirm: ") == 'YES':
                        self.controller.delete(port)
                        for port_name in self.controller.port_names():
                            print(port_name)
                        port=None

    def load_portfolio(self):
        files = os.listdir("data/")

        for i in range(0, len(files)):
            files[i] = os.path.splitext(files[i])[0]
            print(i, files[i])

        file = int(input("Which file: "))
        for text in self.controller.load_portfolio(files[file]):
            print(text)
