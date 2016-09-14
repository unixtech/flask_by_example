from flask import Flask, render_template, request, url_for
from config import Config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import os

import requests
import re
import nltk
import operator
from collections import Counter
from lxml import html
from stop_words import stops



app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result

@app.route('/', methods=['GET', 'POST'])
def hello():
    errors = []
    results = {}
    if request.method == "POST":
        try:
            url = request.form['url']
            r = requests.get(url)
            print(r.text)
        except:
            errors.append('Unable to get URL')
    return render_template('index.html', errors=errors, results=results)

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(host="10.0.10.32", port=8000)
