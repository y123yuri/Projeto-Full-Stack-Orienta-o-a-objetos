from app import app, db
from flask import render_template, redirect, request, flash, session, url_for, jsonify
from app.models.tables import *
from werkzeug.security import check_password_hash, generate_password_hash
import json
import re

@app.route('/')
@app.route('/home')
def home():
    restaurantes_lista = Restaurantes.query.all()
    for restaurante in restaurantes_lista:
        # Remove colchetes e aspas extras das URLs
        restaurante.fotos = restaurante.fotos.strip("[]").replace("'", "").split(",") 
    return render_template('home.html', restaurantes = restaurantes_lista)



@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('q', '').strip().lower()
    
    if len(termo) < 3:
        return jsonify([])  # Retorna lista vazia se não houver termo

    # Filtrando restaurantes que contêm o termo digitado
    restaurantes_filtrados = Restaurantes.query.filter(Restaurantes.nome.ilike(f"%{termo}%")).all()

    # Convertendo os resultados para JSON
    resultados = [{"id": r.id, "nome": r.nome} for r in restaurantes_filtrados]

    return jsonify(resultados)

@app.route('/tipos_comida', methods=['GET'])
def tipos_comida():
    tipos = Restaurantes.query.with_entities(Restaurantes.tipo).distinct().all()
    tipos_lista = [tipo[0].capitalize() for tipo in tipos]  # Convertendo tuplas para lista
    return jsonify(tipos_lista)


@app.route('/filtro', methods=['GET'])
def filtro():
    termo = request.args.get('q', '').strip().lower()
    tipo = request.args.get('tipo', '').strip().lower()

    query = Restaurantes.query

    if termo:
        query = query.filter(Restaurantes.nome.ilike(f"%{termo}%"))

    if tipo:
        query = query.filter(Restaurantes.tipo.ilike(f"%{tipo}%"))

    restaurantes_filtrados = query.all()

    resultados = [{"id": r.id, "nome": r.nome} for r in restaurantes_filtrados]

    return jsonify(resultados)

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
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
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
    try:
        fotos = json.loads(restaurante.fotos)  # Se já estiver como string no banco
    except json.JSONDecodeError:
        fotos = restaurante.fotos.strip("[]").replace("'", "").split(", ") 
    import re

    if restaurante.link_maps and "google.com/maps" in restaurante.link_maps:
        match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', restaurante.link_maps)
        place_id_match = re.search(r'!1s([^!]+)', restaurante.link_maps)

        if match:
            lat, lon = match.groups()
            embed_url = f"https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1000!2d{lon}!3d{lat}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1"
            restaurante.link_maps = embed_url
        
        elif place_id_match:
            place_id = place_id_match.group(1)
            embed_url = f"https://www.google.com/maps/embed?pb=!1m2!1m1!1s{place_id}"
            restaurante.link_maps = embed_url
        
        else:
            print("Erro: Link do Google Maps inválido.")
    else:
        print("Nenhum link de mapa disponível.")
    print("URL gerada para embed:", restaurante.link_maps)




    return render_template('restaurante.html', restaurante=restaurante, comentarios_fake = comentarios_processados, comentarios= comentarios_reais,fotos=json.dumps(fotos))


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





@app.route('/adicionar_comentario', methods=['POST'])
def adicionar_comentario():
    if 'usuario_id' not in session:
        return jsonify({"error": "Usuário não autenticado"}), 403

    usuario_id = session['usuario_id']
    restaurante_id = request.form.get('restaurante_id')
    conteudo = request.form.get('conteudo').strip()

    if not conteudo:
        return jsonify({"error": "Comentário não pode estar vazio"}), 400

    usuario = User.query.get(usuario_id)  # Obtendo o usuário autenticado
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Criando e adicionando o comentário ao banco de dados
    novo_comentario = Comentarios(
        conteudo=conteudo,
        user_id=usuario_id,
        likes=0,  # Comentário inicia sem curtidas
        restaurante_id=restaurante_id
    )

    db.session.add(novo_comentario)
    db.session.commit()

    # Retornando o comentário recém-criado para exibição no frontend
    return jsonify({
        "id": novo_comentario.id,
        "username": usuario.username,
        "conteudo": novo_comentario.conteudo
    })
