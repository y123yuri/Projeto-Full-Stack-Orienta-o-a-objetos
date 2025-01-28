from app import app
from flask import render_template, redirect, request

@app.route('/')
@app.route('/index')
def index():
    return "aOalad maundo"



@app.route('/login', methods=['POST'])
def login():

    nome = request.form.get('nome')
    senha = request.form.get('senha')
    print(nome)
    print(senha)
    return render_template('login.html')