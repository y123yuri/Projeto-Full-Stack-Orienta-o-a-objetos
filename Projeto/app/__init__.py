from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///data/storage.db'
# db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'PROJETO_OO'

from app import routes
