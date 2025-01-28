from app import app
from flask import render_template, redirect, request
from app.funcoes import criar_json, salvar_dados_json, verificar_user

@app.route('/')
@app.route('/index')
def index():
    return "aOabvgffhrftlad maundo"


criar_json = criar_json() # cria o json

@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        
        
        usuario = request.form.get('usuario')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        

        novo_usuario = {
            'nome': nome,
            'usuario': usuario,
            'email': email,
            'senha': senha,
        }
        
        verificacao = verificar_user(usuario=usuario)
        if verificacao != True:
            salvar_dados_json(novo_usuario) # salva os dados coletados no json
            return 'Usário cadastrado com sucesso!'
        else:
            flash('O nome de usuário já foi cadastrado!', 'error') 
    return render_template('cadastro.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        nome = request.form.get('usuario')
        senha = request.form.get('senha')
        print(nome)
        print(senha)
    return render_template('login.html')
    #fazer logica 