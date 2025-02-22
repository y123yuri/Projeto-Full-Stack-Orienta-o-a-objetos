import unidecode
import ast  
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app import db, app  # Importando app e db corretamente
from app.models.tables import Restaurantes, ComentariosFake
from random import randint

nomes = [
    "Igor Domingues", "Marcos Coelho", "Fábio Almeida", "Isabela Tavares", "Wagner Monteiro",
    "Elisa Correia", "Eduardo Reis", "Michele Ferreira", "Larissa Andrade", "Ricardo Pinto",
    "Ana Cavalcanti", "Sérgio Carvalho", "Gustavo Costa", "Ana Vieira", "Fernanda Drummond",
    "Sabrina Almeida", "Yasmin Lima", "Otávio Lima", "Karen Lopes", "Alex Correia",
    "Renata Gomes", "Caio Cavalcanti", "Isabela Araújo", "Igor Machado", "Marcos Pinto",
    "Patrícia Drummond", "Zilda Pereira", "Yuri Reis", "Zilda Costa", "Gabriel Teixeira",
    "Orlando Martins", "Fábio Nascimento", "Isabela Cavalcanti", "Gabriel Teixeira", "Larissa Vieira",
    "Zuleica Gomes", "Fernanda Correia", "Leonardo Mendes", "Patrícia Pacheco", "Nelson Guimarães",
    "André Nascimento", "Larissa Fonseca", "Patrícia Campos", "Bianca Cavalcanti", "João Costa",
    "Bianca Correia", "Alex Gomes", "Eduardo Costa", "João Ferreira", "Karen Correia"
]



tipos = ["churrasco", "japonesa", "italiana", "arabe", "chinesa",
 "mexicana", "nordestina", "feijoada", "mineira", "baiana",
 "vegetariana", "vegana", "tailandesa", "hamburguer",
 "francesa", "pizza", "coreana"]



with open('models.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Separar os blocos de listas usando o delimitador @%
blocos = conteudo.split("@%")

listas_processadas = []

for bloco in blocos:
    bloco = bloco.strip()  # Remover espaços extras
    print(blocos)
    try:
        
        # Converter string para uma lista real usando ast.literal_eval (mais seguro que eval)
        lista = ast.literal_eval(bloco)
        listas_processadas.append(lista)
    except:
        print('quebrei')
        break



contador_listas = 0



for lista_tipo in listas_processadas:
    with app.app_context():
        if lista_tipo == []:
            print(f"Nao foi a {tipos[contador_listas]}")
            contador_listas+=1
            continue
        for restaurante in lista_tipo:

            tipo = tipos[contador_listas]
            nome_restaurante = restaurante[0]
            if  ':' in nome_restaurante: #'-' in nome_restaurante or
                pos = nome_restaurante.find(':')
                nome_restaurante = nome_restaurante[0:pos].strip()
            elif '-' in nome_restaurante :
                pos = nome_restaurante.find('-')
                nome_restaurante = nome_restaurante[0:pos].strip()
            elif '!' in nome_restaurante:
                pos = nome_restaurante.find('!')
                nome_restaurante = nome_restaurante[pos+1:] .strip()
            else:
                pass
                
                
            endereco = restaurante[1]
            telefone = restaurante[2]
            descricao = restaurante[3]
            numero_avaliacao = restaurante[4]
            comentarios = restaurante[5]
            lista_horario = restaurante[6]
            lista_fotos = restaurante[7]
            maps = restaurante[8]

            lista_horario = f'{lista_horario}'
            lista_fotos = f'{lista_fotos}'
            print(tipo,nome_restaurante, telefone)
            novo_restaurante = Restaurantes(
                    nome=nome_restaurante,
                    tipo=tipo,
                    endereco=endereco,
                    telefone=telefone,
                    descricao=descricao,
                    avaliacoes=numero_avaliacao,
                    horario=lista_horario,
                    fotos=lista_fotos,
                    link_maps=maps
                )
            db.session.add(novo_restaurante)
            db.session.commit()
            restaurante = Restaurantes.query.filter_by(nome=nome_restaurante).first()

            if restaurante:
                restaurante_id = restaurante.id  # Pegando o ID do restaurante
                print(f"ID do restaurante: {restaurante_id}")
            else:
                print("Restaurante não encontrado")
            for comentario in comentarios:
                x = randint(0,len(nomes)-1)
                novo_comentario = ComentariosFake(
                    conteudo = comentario,
                    nome = nomes[x],
                    restaurante_id = restaurante_id
                )
                db.session.add(novo_comentario)
                db.session.commit()
                print("Restaurante adicionado com sucesso!")
                    # Adicionando ao banco de dados
        
            

    contador_listas+=1

    






