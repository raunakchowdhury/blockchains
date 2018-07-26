from app import app
from flask import render_template, redirect, url_for
import requests

@app.route('/')
def home():
    return 'Welcome to my blockchain website!'

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/transactions/create')
def create_transactions():
    return render_template('transactions.html')

@app.route('/transactions')
def transactions_list():
    #requested_info = requests.get('http://{}'.format(url_for('get_transactions')))
    return redirect(url_for('get_transactions'))#requested_info 
