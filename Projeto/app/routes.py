from app import app, db
from flask import render_template, redirect, request, flash, session, url_for
from app.models.tables import User,Perfil,Restaurantes
from werkzeug.security import check_password_hash, generate_password_hash


@app.route('/')
def home():
    return "aOabvgffhrftlad maundo"




@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            usuario = request.form.get('usuario').lower().strip()
            nome = request.form.get('nome').strip()
            email = request.form.get('email').lower().strip()
            senha = request.form.get('senha').strip()
            
            # Verifica se já existe um usuário com o mesmo username ou email
            if User.query.filter_by(username=usuario).first() is not None:
                flash("Nome de usuário já existe!", "error")
                return redirect(url_for('cadastro'))
            
            if User.query.filter_by(email=email).first() is not None:
                flash("E-mail já cadastrado!", "error")
                return redirect(url_for('cadastro'))

            # Criptografa a senha antes de salvar no banco
            senha_hash = generate_password_hash(senha)

            user = User(username=usuario, name=nome, password=senha_hash, email=email) #criar no banco de dados

            perfil = Perfil(user_id=usuario, bio=None,avatar=None)
            db.session.add(perfil)
            db.session.add(user)
            db.session.commit()


            return redirect(url_for('login'))

        return render_template('cadastro.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if session:
        return redirect(url_for('home'))
    else:
        if request.method == 'POST':
            info = request.form.get('usuario').strip().lower()  # Permite login com email ou username
            senha = request.form.get('senha')
            print(info,senha)
            # Buscar pelo username ou email
            usuario = User.query.filter((User.username == info) | (User.email == info)).first()

            if usuario and check_password_hash(usuario.password, senha):
                session['usuario_id'] = usuario.id  # Armazena o ID do usuário na sessão
                session['usuario_nome'] = usuario.username  # opcional: pode armazenar o nome também
                
                return redirect(url_for('perfil'))  # redireciona para o perfil
            else:
                return "Usuário ou senha incorretos"
        
        return render_template('login.html')  # página de login

    

@app.route('/logout')
def logout():
    session.clear()  # Limpa a sessão
    return redirect(url_for('home'))  # Redireciona para a página de login



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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))  # Se não estiver logado, redireciona para login
    usuario = User.query.get(session['usuario_id'])  # Busca o usuário no banco de dados
    
    if not usuario:
        session.clear()  # Se o usuário não existir mais, limpa a sessão
        flash("Sessão inválida. Faça login novamente.", "error")
        return redirect(url_for('login'))

    perfil = Perfil.query.filter_by(user_id=usuario.username).first()
        
    return render_template('perfil.html', usuario=usuario, perfil=perfil)



    