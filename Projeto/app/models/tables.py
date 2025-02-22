from app import db
from sqlalchemy.ext.declarative import declared_attr

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
    descricao = db.Column(db.String(5000))
    link_maps = db.Column(db.String(300))
    

    def __init__(self, nome, avaliacoes, tipo, endereco, horario, fotos,telefone, descricao, link_maps):

        self.nome = nome
        self.endereco = endereco
        self.avaliacoes = avaliacoes
        self.fotos = fotos
        self.horario = horario
        self.tipo = tipo
        self.telefone = telefone
        self.descricao = descricao
        self.link_maps = link_maps
        

    def __repr__(self):
        return f"<Restaurante {self.nome}>"



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

class ComentarioBase(db.Model):
    __abstract__ = True  # Define esta classe como abstrata (não será criada como tabela)
    
    id = db.Column(db.Integer, primary_key=True)
    conteudo = db.Column(db.Text, nullable=False)

    @declared_attr
    def restaurante_id(cls):
        return db.Column(db.Integer, db.ForeignKey('restaurantes.id'), nullable=False)

    @declared_attr
    def restaurante(cls):
        return db.relationship("Restaurantes", foreign_keys=[cls.restaurante_id])

    def __repr__(self):
        return f"<Comentario {self.id}>"


class Comentarios(ComentarioBase):
    __tablename__ = "comentarios"

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    likes = db.Column(db.Integer, default=0)

    user = db.relationship("User", foreign_keys=[user_id])

    def __init__(self, conteudo, user_id, restaurante_id, likes=0):
        self.conteudo = conteudo
        self.user_id = user_id
        self.restaurante_id = restaurante_id
        self.likes = likes

    def __repr__(self):
        return f"<Comentario {self.id} - User {self.user_id}>"



class ComentariosFake(ComentarioBase):
    __tablename__ = "comentarios_fake"

    nome = db.Column(db.String(100), nullable=False)

    def __init__(self, nome, conteudo, restaurante_id):
        self.nome = nome
        self.conteudo = conteudo
        self.restaurante_id = restaurante_id

    def __repr__(self):
        return f"<ComentarioFake {self.id} - {self.nome}>"



# Herança: ComentarioBase → Comentarios (Especialização da classe base para comentários reais).
# Herança: ComentarioBase → ComentariosFake (Especialização da classe base para comentários falsos).
# Composição: User → Perfil (Cada usuário tem um perfil exclusivo, que só existe junto com o usuário).
# Associação: Restaurantes ↔ Comentarios (Um restaurante pode ter vários comentários reais).
# Associação: Restaurantes ↔ ComentariosFake (Um restaurante pode ter vários comentários falsos).
# Associação: User ↔ Comentarios (Um usuário pode fazer vários comentários).
#Dependência: User → Perfil (O usuário pode existir sem o perfil, mas o perfil depende do usuário para existir).