from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))  # caminho base do projeto
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, '..', 'data', 'storage.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'PROJETO_OO'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes 


#flask db init,flask db migrate

#toda vez que a gente mudar no banco de dados, a gente da esse comando flask db upgrade