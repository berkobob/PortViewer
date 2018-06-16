from flask import Flask, render_template

app = Flask(__name__)
contoller = None

def startWebView(new_controller):
    global controller
    controller=new_controller
    app.run(debug=True)

@app.route('/')
def hello_method():
    global controller
    ports=controller.port_names()
    return render_template('home.html', ports=ports)

@app.route('/<port>/')
def view_port(port):
    global controller
    tickers=controller.get_port(port)
    return render_template('portfolio.html',port=port, tickers=tickers)

if __name__ == '__main__':
    from src.controller.portfolios import Controller
    from src.model.data import Data
    startWebView(Controller(Data()))