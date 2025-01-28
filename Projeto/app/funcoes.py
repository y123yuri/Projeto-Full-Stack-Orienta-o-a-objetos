import json
import os 

# Caminho para a pasta 'data' e o arquivo 'usuarios.json'


data_user = 'app/data/usuarios.json'  # caminho para o arquivo JSON

# cria o arquivo JSON vazio se ele não existir
def criar_json():
    if not os.path.exists(data_user):
        with open(data_user, 'w') as arquivo:
            json.dump([], arquivo)

# lê os dados do arquivo JSON
def carregar_dados_json():
    if os.path.exists(data_user):
        with open(data_user, 'r') as arquivo:
            return json.load(arquivo)
    return []

# salva os dados no arquivo JSON
def salvar_dados_json(novo_usuario):
    # carrega os dados existentes
    dados = carregar_dados_json()
    # adiciona o novo usuário
    dados.append(novo_usuario)
    # salva de volta no arquivo
    with open(data_user, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def verificar_user(usuario):
    with open(data_user, 'r') as arquivo:
        usuarios = json.load(arquivo)  

    # verifica se o usuário existe
    for user in usuarios:
        if user.get('nome') == usuario:  #usuario foi encontrado, tem que travar o sistema
            print(f"Usuário {usuario} encontrado!")
            return True

    print(f"Usuário {usuario} não encontrado.")
    return False
