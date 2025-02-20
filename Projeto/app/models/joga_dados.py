import unidecode
import ast  
import time

tipos = ["churrasco", "japonesa", "italiana", "arabe", "chinesa",
 "mexicana", "nordestina", "feijoada", "mineira", "baiana",
 "vegetariana", "vegana", "tailandesa", "hamburguer",
 "francesa", "pizza", "coreana", "peruana", "alema"]



with open('models.txt', 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Separar os blocos de listas usando o delimitador @%
blocos = conteudo.split("@%")

listas_processadas = []

for bloco in blocos:
    bloco = bloco.strip()  # Remover espaços extras

    try:
        # Converter string para uma lista real usando ast.literal_eval (mais seguro que eval)
        lista = ast.literal_eval(bloco)
        listas_processadas.append(lista)
    except:
        print('quebrei')
        break



contador_listas = 0



for lista_tipo in listas_processadas:
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
        comentario = restaurante[5]
        lista_horario = restaurante[6]
        lista_fotos = restaurante[7]
        maps = restaurante[8]

        

        print(tipo,nome_restaurante, telefone, lista_horario)

            

    contador_listas+=1

    






