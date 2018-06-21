from flask import Flask, render_template, request,url_for, redirect

app = Flask(__name__)
contoller = None
ascending = True

def startWebView(new_controller):
    global controller
    controller = new_controller
    app.run('0.0.0.0', port=80, debug=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        controller.new_port(request.form['name'])
    return render_template('home.html', ports=controller.port_names())

@app.route('/<port>/')
def port_view(port):
    global controller
    ports = controller.port_names()
    tickers=controller.get_port(port)
    return render_template('port.html', ports=ports, tickers=tickers, page=port)

@app.route('/<col>/<port>/')
def sort(col, port):
    global ascending
    tickers = controller.sort(port, col, ascending)
    ascending = not ascending
    return redirect('/'+port)

@app.route('/update/<port>/')
def update(port):
    controller.update(port)
    return redirect('/'+port)

@app.route('/add/<port>', methods=['POST'])
def add_ticker(port):
    controller.add_ticker(port, list(request.form.values()))
    return redirect('/'+port)

if __name__ == '__main__':
    import sys
    sys.path.append('c:\\Users\\aleve\\Documents\\src\\PortViewer\\src\\controller')
    for path in sys.path:
        print(path)
    from controller.portfolios import Controller
    from src.model.data import Data
    startWebView(Controller(Data()))
    