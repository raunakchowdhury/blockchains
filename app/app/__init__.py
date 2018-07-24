from flask import Flask, request, jsonify, render_template, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'whomst gonn guess this?'

from app import api, routes

#if __name__ == '__main__':
#    app.run(debug=True)
