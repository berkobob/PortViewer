import argparse
from src.model.data import Data
from src.controller.portfolios import Controller as application

#if __name__ == '__main__':
def main():
    parser = argparse.ArgumentParser(
        description="View portfolio prices",
        epilog="Changes to come."
    )
    parser.add_argument('-v', '--verbose', help="Increase the level of verbosity", action="store_true")
    parser.add_argument('-s', '--square', help="Returns the square of the given number", type=int)
    parser.add_argument('-m', '--mode', help="Use Command line, Web or Desktop", default='w')
    #parser.add_argument('-m', '--mode', help="Use Command line, Web or Desktop", choices=['c','w','d'])

    args=parser.parse_args()

    if args.mode:
        mode = args.mode[0].lower()
        if mode == 'd':
            print("Desktop mode not yet implemented")
        elif mode == 'w':
            from src.view.app import startWebView
            startWebView(application(Data()))
        elif mode == 'c':
            from src.view.commandline import View
            View(application(Data()))
        else:
            print("The valid modes are Command line (c), Web (w) or Desktop (d)")

    if args.square:
        print(args.square**2)

if __name__ == '__main__':
    main()
