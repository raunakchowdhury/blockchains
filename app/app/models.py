from app import db
import os, csv

base_dir = os.path.abspath(os.path.dirname(__file__))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80)) #instance vars for User
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    #amount = db.Column(db.String(80))

    def __init__(self,user,email,password):
        self.user = user
        self.email = email
        self.password = password
        #self.amount = amount
