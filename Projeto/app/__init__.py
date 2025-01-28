from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'PROJETO_OO'

from app import routes
