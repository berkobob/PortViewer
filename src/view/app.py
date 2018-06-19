from flask import Flask, render_template, request

app = Flask(__name__)
contoller = None

def startWebView(new_controller):
    global controller
    controller = new_controller
    app.run(debug=True)

@app.route('/')
@app.route('/<port>/', methods=['GET', 'POST'])
def hello_method(port=None):
    global controller

    if 'update' in request.form.keys():
        controller.update(port)

    tickers=[]
    ports = controller.port_names()
    if port:
        tickers=controller.get_port(port)
        
    return render_template('home.html', ports=ports, tickers=tickers)

if __name__ == '__main__':
    import sys
    sys.path.append('c:\\Users\\aleve\\Documents\\src\\PortViewer\\src\\controller')
    for path in sys.path:
        print(path)
    from controller.portfolios import Controller
    from src.model.data import Data
    startWebView(Controller(Data()))
    