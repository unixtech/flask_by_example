from flask import Flask
from config import Config, DevelopmentConfig
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Result

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(host="10.0.10.32", port=8000)
