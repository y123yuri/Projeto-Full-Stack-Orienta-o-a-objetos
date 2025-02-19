from app import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), unique=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.email = email
        self.name = name

    def __repr__(self):
        return f"<User {self.username}>"


class Comentarios(db.Model):
    __tablename__ = "comentarios"

    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurante_id = db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)

    # Relacionamentos
    restaurante = db.relationship("Restaurantes", foreign_keys=[restaurante_id])
    user = db.relationship("User", foreign_keys=[user_id])

    def __init__(self, conteudo, user_id, likes, restaurante_id):
        self.conteudo = conteudo
        self.user_id = user_id
        self.likes = likes
        self.restaurante_id = restaurante_id

    def __repr__(self):
        return f"<Comentario {self.id}>"


class Restaurantes(db.Model):
    __tablename__ = "restaurantes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(60), nullable=False)
    avaliacoes = db.Column(db.Text) 
    tipo = db.Column(db.String(60))
    endereco = db.Column(db.String(120))
    horario = db.Column(db.String(60))
    fotos = db.Column(db.String(120))  
    telefone = db.Column(db.String(30))
    

    def __init__(self, nome, avaliacoes, tipo, endereco, horario, fotos,telefone):

        self.nome = nome
        self.endereco = endereco
        self.avaliacoes = avaliacoes
        self.fotos = fotos
        self.horario = horario
        self.tipo = tipo
        self.telefone = telefone

    def __repr__(self):
        return f"<Restaurante {self.nome}>"

class Usuario_fake(db.Model):
    __tablename__="fakes"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    avaliacao = db.Column(db.String(1000),nullable=False)

    def __init__(self, nome, avaliacao):
        self.nome = nome
        self.avaliacao = avaliacao


    def __repr__(self):
        return f"<Perfil {self.nome}"



class Perfil(db.Model):
    __tablename__ = "perfis"

    id = db.Column(db.Integer, primary_key=True)
    bio = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(120), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    # Relacionamento
    user = db.relationship("User", backref=db.backref("perfil", uselist=False, cascade="all, delete-orphan"))

    def __init__(self, bio, avatar, user_id):
        self.bio = bio
        self.avatar = avatar
        self.user_id = user_id

    def __repr__(self):
        return f"<Perfil {self.id} - User {self.user_id}>"
