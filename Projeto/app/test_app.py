import pytest
from app import app, db
from app.models.tables import User, Restaurantes, Comentarios, Perfil
from werkzeug.security import generate_password_hash


@pytest.fixture
def client():
    """Configura um cliente de testes para o Flask sem afetar o banco de produção."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Banco de testes separado
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Cria tabelas apenas no banco de testes
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Apaga apenas o test.db, sem afetar o banco principal


def test_home(client):
    """Testa se a página inicial carrega corretamente."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"restaurantes" in response.data

def test_buscar_restaurante(client):
    """Testa a busca de restaurantes."""
    with app.app_context():
        restaurante = Restaurantes(nome="Pizza Hut", tipo="Pizza", fotos="['foto1.jpg']", endereco="Rua X, 123", horario="9h-22h", telefone="(11) 1234-5678", descricao="Melhor pizza da cidade!", link_maps="https://maps.google.com/example", avaliacoes="5")
        db.session.add(restaurante)
        db.session.commit()

    response = client.get('/buscar?q=pizza')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]["nome"] == "Pizza Hut"



def test_tipos_comida(client):
    """Testa a listagem dos tipos de comida."""
    with app.app_context():
        db.session.add(Restaurantes(nome="McDonald's", tipo="Fast Food", fotos="['foto.jpg']", avaliacoes="4 estrelas", endereco="Avenida Central, 200", horario="10h-23h", link_maps="https://maps.google.com/example", telefone="(11) 9876-5432", descricao="Famoso por seus lanches!"))
        db.session.add(Restaurantes(nome="Sushi House", tipo="Japonesa", fotos="['foto.jpg']", avaliacoes="4 estrelas", endereco="Avenida Central, 200", horario="10h-23h", link_maps="https://maps.google.com/example", telefone="(11) 9876-5432", descricao="Famoso por seus lanches!"))
        db.session.commit()

    response = client.get('/tipos_comida')
    assert response.status_code == 200
    json_data = response.get_json()
    assert "Fast food" in json_data
    assert "Japonesa" in json_data


def test_filtro(client):
    """Testa a funcionalidade de filtro de restaurantes."""
    with app.app_context():
        db.session.add(Restaurantes(nome="Burger King", tipo="Fast Food", fotos="['foto.jpg']", avaliacoes="4.5 estrelas", endereco="Rua das Lojas, 50", horario="11h-22h", telefone="(11) 9000-0000", descricao="Hambúrgueres famosos!", link_maps="https://maps.google.com/example"))
        db.session.add(Restaurantes(nome="Dominos", tipo="Pizza", fotos="['foto.jpg']",  avaliacoes="4.5 estrelas", endereco="Rua das Lojas, 50", horario="11h-22h", telefone="(11) 9000-0000", descricao="Hambúrgueres famosos!", link_maps="https://maps.google.com/example" ))
        db.session.commit()

    response = client.get('/filtro?q=king&tipo=fast food')
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) > 0
    assert json_data[0]["nome"] == "Burger King"


def test_cadastro_usuario(client):
    """Testa o cadastro de um usuário."""
    response = client.post('/cadastro', data={
        'usuario': 'testuser',
        'nome': 'Test User',
        'email': 'testuser@example.com',
        'senha': '123456'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"login" in response.data


def test_login(client):
    """Testa o login de um usuário existente."""
    with app.app_context():
        senha_hash = generate_password_hash("123456")
        usuario = User(username="testuser", name="Test User", email="testuser@example.com", password=senha_hash)
        db.session.add(usuario)
        db.session.commit()

    response = client.post('/login', data={
        'usuario': 'testuser',
        'senha': '123456'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"perfil" in response.data


def test_logout(client):
    """Testa o logout de um usuário."""
    with app.app_context():
        senha_hash = generate_password_hash("123456")
        usuario = User(username="testuser", name="Test User", email="testuser@example.com", password=senha_hash)
        db.session.add(usuario)
        db.session.commit()

    client.post('/login', data={'usuario': 'testuser', 'senha': '123456'}, follow_redirects=True)

    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"login" in response.data


def test_perfil(client):
    """Testa o acesso ao perfil do usuário."""
    with app.app_context():
        senha_hash = generate_password_hash("123456")
        usuario = User(username="testuser", name="Test User", email="testuser@example.com", password=senha_hash)
        db.session.add(usuario)
        db.session.commit()

    client.post('/login', data={'usuario': 'testuser', 'senha': '123456'}, follow_redirects=True)

    response = client.get('/perfil')
    assert response.status_code == 200
    assert b"perfil" in response.data


def test_restaurante_detalhes(client):
    """Testa o acesso à página de detalhes de um restaurante."""
    with app.app_context():
        restaurante = Restaurantes(
            nome="KFC",
            tipo="Fast Food",
            fotos="['foto.jpg']",
            avaliacoes="4 estrelas",
            endereco="Rua das Fritas, 88",
            horario="10h-23h",
            telefone="(11) 1234-0000",
            descricao="Famoso frango frito!",
            link_maps="https://maps.google.com/example"
        )
    db.session.add(restaurante)
    db.session.commit()

    # Garante que a sessão do SQLAlchemy mantém o objeto acessível
    db.session.refresh(restaurante)


    response = client.get(f'/restaurante/{restaurante.id}')
    assert response.status_code == 302  # Redireciona para login porque não está autenticado

    with app.app_context():
        senha_hash = generate_password_hash("123456")
        usuario = User(username="testuser", name="Test User", email="testuser@example.com", password=senha_hash)
        db.session.add(usuario)
        db.session.commit()

    client.post('/login', data={'usuario': 'testuser', 'senha': '123456'}, follow_redirects=True)

    response = client.get(f'/restaurante/{restaurante.id}')
    assert response.status_code == 200
    assert b"KFC" in response.data


def test_adicionar_comentario(client):
    """Testa a adição de um comentário a um restaurante."""
    with app.app_context():
        usuario = User(
            username="testuser", 
            email="test@example.com", 
            password=generate_password_hash("123456"), 
            name="Test User"
        )
        restaurante = Restaurantes(
    nome="McDonalds",
    tipo="Fast Food",
    fotos="['foto.jpg']",
    avaliacoes="4.5 estrelas",
    endereco="Avenida Principal, 10",
    horario="8h-22h",
    telefone="(11) 9999-9999",
    descricao="Famoso por seus lanches!",
    link_maps="https://maps.google.com/example"
)

        db.session.add(usuario)
        db.session.add(restaurante)
        db.session.commit()

    client.post('/login', data={'usuario': 'testuser', 'senha': '123456'}, follow_redirects=True)

    response = client.post('/adicionar_comentario', data={
        'restaurante_id': restaurante.id,
        'conteudo': 'Ótima comida!'
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["conteudo"] == "Ótima comida!"

