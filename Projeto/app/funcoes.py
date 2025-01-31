# import os
# import json

# # define o caminho absoluto do arquivo JSON
# base_dir = os.path.abspath(os.path.dirname(__file__))
# # data_user = os.path.join(base_dir, 'data/usuarios.json')

# # cria o arquivo JSON vazio se ele não existir
# def criar_json():
#     if not os.path.exists(data_user):
#         with open(data_user, 'w') as arquivo:
#             json.dump([], arquivo)

# # lê os dados do arquivo JSON
# def carregar_dados_json():
#     if os.path.exists(data_user):
#         with open(data_user, 'r') as arquivo:
#             return json.load(arquivo)
#     return []

# # salva os dados no arquivo JSON
# def salvar_dados_json(novo_usuario):
#     # carrega os dados existentes
#     dados = carregar_dados_json()
#     # adiciona o novo usuário
#     dados.append(novo_usuario)
#     # salva de volta no arquivo
#     with open(data_user, 'w') as arquivo:
#         json.dump(dados, arquivo, indent=4)

# def verificar_user(usuario, email):
#     if os.path.exists(data_user):
#         with open(data_user, 'r') as arquivo:
#             usuarios = json.load(arquivo)

#         # verifica se o nome de usuário ou o e-mail já existe
#         for user in usuarios:
#             if user.get('usuario') == usuario:
#                 print(f"Usuário {usuario} já está cadastrado!")
#                 return True # nome de usuário já existe
#             if user.get('email') == email:
#                 print(f"E-mail {email} já está cadastrado!")
#                 return True  # email já existe

#     print(f"Usuário {usuario} e e-mail {email} não encontrados.")
#     return False
