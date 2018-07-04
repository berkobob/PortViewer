import os
from src.view.decorators import requires_login
from flask import Flask, render_template, request,url_for, redirect, session
from passlib.hash import pbkdf2_sha512
from src.controller.portfolios import Controller
from src.model.data import Data

app = Flask(__name__)
app.secret_key = os.urandom(24)
controller = Controller(Data())
ascending = True

def startWebView(new_controller):
    global controller
    controller = new_controller
    app.run('0.0.0.0')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if pbkdf2_sha512.verify(request.form['password'],
        '$pbkdf2-sha512$25000$H6N0LqV0rhXiPOc8R.jduw$3QHAzZkv76ej5bWWzZ9nWH5WmXrttRMwYEmo8xKvIvXHZhWNKVPXpv2JYZqyxSuTdi4DzcSrDbFovQCJZOJyzQ'):
            session['login'] = True
            return redirect('/')
        else:
            session['login'] = False
    return render_template("login.html")

@app.route('/', methods=['GET', 'POST'])
@requires_login
def home():
    if request.method == "POST":
        controller.new_port(request.form['name'])
    return render_template('home.html', ports=controller.port_names())

@app.route('/<port>/', methods=['GET', 'POST'])
@requires_login
def port_view(port):
    if request.method == 'POST':
        print (request)
        return render_template('home.html', ports=controller.port_names())

    if port == 'login':
        print("Ah no. Not this again")

    ports = controller.port_names()
    tickers=controller.get_port(port)
    return render_template('port.html', ports=ports, tickers=tickers, page=port)

@app.route('/<col>/<port>/')
@requires_login
def sort(col, port):
    global ascending
    tickers = controller.sort(port, col, ascending)
    ascending = not ascending
    return redirect('/'+port)

@app.route('/update/<port>/')
@requires_login
def update(port):
    controller.update(port)
    return redirect('/'+port)

@app.route('/add/<port>', methods=['POST'])
@requires_login
def add_ticker(port):
    controller.add_ticker(port, list(request.form.values()))
    return redirect('/'+port)

@app.route('/del/<port>')
@requires_login
def delete(port):
    controller.delete(port)
    return redirect('/')

@app.route('/del/<port>/<ticker>')
@requires_login
def del_ticker(port, ticker):
    controller.del_ticker(port,ticker)
    return redirect('/'+port)

if __name__ == '__main__':
    app.run()