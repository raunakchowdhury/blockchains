from app import app, db
from flask import session, render_template, request, flash
from models import *
from routes import create_transactions

@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/account/created', methods=['GET','POST'])
def create_account():
    user = request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('password')

    account = User(user,email,password)
    session['user'] = account.user #keeps track of what user is logged in
    db.session.add(account) #stores into RAM
    db.session.commit() #commits all additions/deletions to the db

    return render_template('base.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    email = request.form.get('email')
    password = request.form.get('password')

    account = User.query.filter_by(user=user,email=email,password=password).first() #returns a Query, a list of elements, and takes the first element
    # account is a User
    #.all() returns in a list
    if account == None:
        flash('Invalid account credentials!')
        #get_flashed_messages()
        return redirect(url_for(sign_up))
    session['user'] = account.user #keeps track of what user is logged in
    return render_template('base.html', user=account.user)
