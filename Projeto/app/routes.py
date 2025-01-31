from app import app, db
from flask import render_template, redirect, request, flash, session, url_for
from app.models.tables import User


@app.route('/')
@app.route('/index')
def index():
    return "aOabvgffhrftlad maundo"




@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        
        
        usuario = request.form.get('usuario')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        user = User(username=usuario, name=nome, password=senha, email=email) #criar no banco de dados
        db.session.add(user)
        db.session.commit()

    return render_template('cadastro.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        

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


    