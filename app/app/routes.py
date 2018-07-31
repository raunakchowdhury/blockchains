from app import app
from flask import render_template, redirect, url_for, session
import requests
from models import *

@app.route('/')
def home():
    return 'Welcome to my blockchain website!'

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/transactions/create/<string:user>')
def create_transactions(user):
    if user == session['user']:
        return render_template('transactions.html', user=user)
    return redirect(url_for(create_account))

@app.route('/transactions/created')
def created_transactions():
    pass


@app.route('/transactions')
def transactions_list():
    #requested_info = requests.get('http://{}'.format(url_for('get_transactions')))
    return redirect(url_for('get_transactions'))#requested_info

def login_required(function):
    account = User.query.filter_by(user=user,email=email,password=password).first() #returns a Query, a list of elements, and takes the first element
