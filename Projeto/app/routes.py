from app import app, db
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from app.models.tables import *
from werkzeug.security import check_password_hash, generate_password_hash

@app.route('/')
@app.route('/home')
def home():
    restaurantes_lista = Restaurantes.query.all()
    for restaurante in restaurantes_lista:
        # Remove colchetes e aspas extras das URLs
        restaurante.fotos = restaurante.fotos.strip("[]").replace("'", "").split(",") 
    return render_template('home.html', restaurantes = restaurantes_lista)




@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if 'usuario_id' in session:
        return redirect(url_for('perfil'))
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
    if 'usuario_id' in session:
        return redirect(url_for('perfil'))
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



@app.route('/restaurante/<int:restaurante_id>')
def restaurante(restaurante_id):
    restaurante = Restaurantes.query.get(restaurante_id)
    comentarios = ComentariosFake.query.filter_by(restaurante_id=restaurante_id).all()
    comentarios_reais = Comentarios.query.filter_by(restaurante_id=restaurante_id).all()

    comentarios_processados = []
    for comentario in comentarios:
        conteudo = comentario.conteudo.strip()
    
        # Se houver um ponto, pegar apenas até o primeiro ponto
        pos = conteudo.find('.')
        if pos != -1:
    
            conteudo = conteudo[:pos+1]  # Pega o conteúdo até o primeiro ponto
        
            # Criar um novo objeto ou atualizar o existente
        comentario.conteudo = conteudo
        comentarios_processados.append(comentario)
    if not restaurante:
        flash("Restaurante não encontrado.", "error")
        return redirect(url_for('home'))
    restaurante.fotos = restaurante.fotos.strip("[]").replace("'", "").split(",") 

    

    return render_template('restaurante.html', restaurante=restaurante, comentarios_fake = comentarios_processados, comentarios= comentarios_reais)


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





@app.route('/adicionar_comentario/<int:restaurante_id>', methods=['POST'])
def adicionar_comentario(restaurante_id):
    data = request.get_json()
    usuario = User.query.get(session['usuario_id'])
    if not data or "conteudo" not in data:
        return jsonify({"status": "error", "message": "Comentário inválido"}), 400

    comentario_texto = data["conteudo"].strip()

    if comentario_texto:
        novo_comentario = Comentarios(
            user_id= usuario.id, # Troque para usuário autenticado se houver login
            conteudo=comentario_texto,
            restaurante_id=restaurante_id,
            likes = 0
        )
        db.session.add(novo_comentario)
        db.session.commit()

        return jsonify({
            "status": "success",
            "user": novo_comentario.user_id,
            "conteudo": novo_comentario.conteudo
        }), 201

    return jsonify({"status": "error", "message": "Comentário vazio"}), 400




