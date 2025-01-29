from app import app
from flask import render_template, redirect, request, flash, session, url_for
from app.funcoes import criar_json, salvar_dados_json, verificar_user, carregar_dados_json


@app.route('/')
@app.route('/index')
def index():
    return "aOabvgffhrftlad maundo"


criar_json() # cria o json 

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
        
        if verificar_user(usuario=usuario, email=email):
            flash('O nome de usuário ou o e-mail já foi cadastrado!', 'error')
        else:
            salvar_dados_json(novo_usuario)  # Salva os dados coletados no JSON
            flash("Cadastro realizado com sucesso!")
            return 'Usuário cadastrado com sucesso!'
    return render_template('cadastro.html')




@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        usuarios = carregar_dados_json() # pega os dados do json

        for user in usuarios: # verifica todos os cadastros já realizados
            if user['usuario'] == usuario and user['senha'] == senha:
                session['usuario'] = user  # Armazena na sessão
                return redirect(url_for('perfil')) # leva pra página de perfil

        return "Usuário ou senha inválidos!"

    return render_template('login.html')
    #fazer logica 

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))


@app.route('/restaurante')
def restaurante():
    restaurante_info = {
        "nome": "Pizzaria Itália",
        "localizacao": "Rua das Flores, 45 - SP",  # isso aqui é so um exemplo, aqui vai os dados dos restaurantes cadastrados
        "avaliacao": 4.8,
        "especialidade": "Pizza Italiana"
    }
    return render_template('restaurante.html', restaurante=restaurante_info)

@app.route('/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    return render_template('perfil.html', usuario=session['usuario'])


    