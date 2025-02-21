import selenium
from selenium import webdriver
import requests
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import random
from bs4 import BeautifulSoup
import re
import os


# Lista dos 20 tipos de comida mais famosos no Brasil
tipos_comida = ["TESTE",
    "churrasco", "comida japonesa", "comida italiana", "comida árabe", "comida chinesa",
    "comida mexicana", "comida nordestina", "feijoada", "comida mineira", "comida baiana",
    "comida vegetariana", "comida vegana", "comida tailandesa", "hambúrguer artesanal",
    "comida francesa", "pizza",  "comida coreana", "comida peruana", "comida alemã"

]



# Configuração do WebDriver
link='https://www.google.com'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"}
requisição=requests.get(link, headers=headers)

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'eager'
# Link de cada professor e matéria
driver = webdriver.Firefox(options=options)
listao = []
lista_tipo_banco = ["churrasco", "japonesa", "italiana", "Árabe", "Chinesa",
 "Mexicana", "Nordestina", "Feijoada", "Mineira", "Baiana",
 "Vegetariana", "Vegana", "Tailandesa", "Hambúrguer",
 "Francesa", "Pizza", "Coreana", "Peruana", "Alemã"]


for comida in tipos_comida:
    listao = []
    """Pesquisa um tipo de comida no Google adicionando 'Brasília'"""
    driver.get("https://www.google.com")
    time.sleep(2)  # Tempo aleatório para carregar a página
    
    # Simular rolagem e interação antes da busca
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    
    # Localiza a barra de pesquisa e digita a consulta
    search_box = driver.find_element(By.NAME, "q")
    ActionChains(driver).move_to_element(search_box).perform()  # Simula movimento do mouse
    search_box.send_keys(f"{comida} Brasília")
    search_box.send_keys(Keys.RETURN)
    
    

    if comida == tipos_comida[0]:    
        try:
            caixinha_capctha = driver.find_element(By.XPATH,'/html/body/div[1]/div')
            print("EU EXISTO", caixinha_capctha)
            if caixinha_capctha:
                time.sleep(15)
                
                
                #resolver o capctha
            else:
                pass
        except:
            pass
    else:
        
        time.sleep(3)  # Tempo aleatório para carregar os resultados
        
        # Captura os primeiros resultados
        
        try:
            resultados = driver.find_elements(By.XPATH, '//*[@id="Odp5De"]/div[1]/div/div/div/div[1]/div[2]/div/div[1]/div[2]/div/h3/g-more-link/a/div')
            if resultados:  # Verifica se encontrou algum resultado
                resultados[0].click()  # Clica no primeiro elemento encontrado
            else:
                search_box = driver.find_element(By.NAME, "q")
                ActionChains(driver).move_to_element(search_box).perform()  # Simula movimento do mouse
                search_box.send_keys(f"{comida} Brasília")
                search_box.send_keys(Keys.RETURN)
                
        except:
            print("nao enconterei o botao de mais lugares, irei para o proximo tipo de comida")
            continue
        time.sleep(3)


        lista_xpath = [
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[4]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[6]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[8]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[10]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[12]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[16]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[18]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[22]/div[2]/div/div/a[2]",
    "/html/body/div[2]/div/div[7]/div[1]/div/div[2]/div[2]/div/div/div/div/div/div/div/div/div[1]/div[3]/div[32]/div[2]/div/div/a[2]",
] 
        
        for xpath in lista_xpath:

            time.sleep(3)
            try:
                
                print(driver.find_element(By.XPATH,xpath))
                time.sleep(3)
                icone_restaurante = driver.find_element(By.XPATH,xpath )  
                icone_restaurante.click()
                time.sleep(8)                                                                       
                html = driver.page_source                                                  
                # Parsear com BeautifulSoup                                                    
                soup = BeautifulSoup(html, "html.parser")                                       
                                                                                                    
                # Buscar os restaurantes
                try:                                          
                    nome_restaurante = soup.find('h2', class_='qrShPb').find_next('span').get_text(strip=True)
                    print(nome_restaurante) 
                    
                    endereco = soup.find('span', class_='LrzXr').get_text(strip=True) 
                    print(endereco) 
                
                    telefone = soup.find('span', class_ ='LrzXr zdqRlf kno-fv').find_next('span').get_text(strip=True)
                    print(telefone)
                    
                    time.sleep(5)
                    try:

                        botao_descricao = driver.find_element(By.XPATH, '//a[@aria-label="mostrar mais"]')
                        time.sleep(5)
                        botao_descricao.click()
                        html = driver.page_source 
                        soup= BeautifulSoup(html,"html.parser") #esse daqui atualiza a pagina
                        descricao_element = soup.find('div', attrs={"jsname": "EvNWZc"})
                        descricao = descricao_element.get_text(strip=True)
                        if descricao[-7:] == '...Mais':
                            raise Exception("Descrição incompleta, tentando novamente...")
                        print("peguei a descricao")
                    except:
                        try:
                            descricao_element = soup.find('div', attrs={"jsname": "EvNWZc"})
                            descricao = descricao_element.get_text(strip=True)
                            if descricao[-7:] == '...Mais':
                                print("nao consegui de novo")
                                raise Exception("Descrição incompleta, tentando novamente...")
                            
                        except:
                            descricao = ''
                            

                    time.sleep(5)

                    html = driver.page_source 
                    soup= BeautifulSoup(html,"html.parser") #esse daqui atualiza a pagina
                    
                    time.sleep(3)

                    
                    print(f'essa e a descricao {descricao}')

                    
                    time.sleep(3)
                    html = driver.page_source 
                    soup= BeautifulSoup(html,"html.parser") #esse daqui atualiza a pagina


                    horarios = soup.find_all('td', class_='SKNSIb')

                    
                    lista_de_horarios = []
                    contador_dia = 0
                    for horario in horarios:      # dia
                        if contador_dia < 8:
                            dia = horario.get_text(strip=True)
                            proximo_td = horario.find_next('td')
                            horarioo = proximo_td.get_text(strip=True)
                            conjunto = dia+' '+horarioo
                            lista_de_horarios.append(conjunto)
                            contador_dia += 1
                        else:
                            break
                    print(lista_de_horarios)
                                        

                    numero_avaliacao = soup.find('span', class_='fzTgPe Aq14fc').get_text(strip=True)
                    print(numero_avaliacao)

                    busca_comentarios = soup.find_all(class_="nNlnIb")
                    comentarios = ''
                    for falas in busca_comentarios:
                        comentarios_tratamento = falas.get_text()
                        comentarios = comentarios_tratamento

                    comentarios = comentarios.replace(comentarios[-28:],'')
                    comentarios = comentarios.replace('""', '@')
                    comentarios = comentarios.replace('"',"")
                    comentarios = comentarios.split("@")
                    print(comentarios)


                    lista_fotos = []
                    fotos1 = soup.find_all('div', class_='vwrQge') 
                    fotos = f'{fotos1}'
                    fotos = fotos.replace('<',"")
                    fotos = fotos.replace('>',"")
                    fotos = fotos.split(",")
                    for url in fotos:
                        pos1 = url.find('(')
                        pos2 = url.find(")")
                        link = url[pos1 + 1:pos2]
                        lista_fotos.append(link)
                        print(link)

                    print(lista_fotos)
                    
                        
                    time.sleep(3)
                    try:
                        links = driver.find_elements(By.CLASS_NAME, 'PbOY2e')
                        if len(links) == 4:
                            time.sleep(5)
                            links[1].click()
                        elif len(links) == 5:
                            time.sleep(5)
                            link[2].click()
                        elif len(links) == 3:
                            time.sleep(5)
                            link[0].click()
                        elif len(links) == 6:
                            time.sleep(5)
                            link[3].click()
                        elif len(links) == 7:
                            time.sleep(5)
                            link[4].click()
                            
                        else:
                            print(len(links))
                            print("Menos de 2 links encontrados com a classe 'PbOY2e'.")

                            continue
                        print('encontrei bota maps')
                        time.sleep(5)

                        link_maps = driver.current_url
                        print(link_maps, 'sou o linkl')
                        driver.back() 
                        time.sleep(5)

                    except:
                        link_maps = ''
                        pass
    
                    
                    restaurante_resultado =[nome_restaurante, endereco, telefone, descricao, numero_avaliacao, comentarios, lista_de_horarios, lista_fotos, link_maps]
                    
                    listao.append(restaurante_resultado)
                        

                    print(restaurante_resultado)
                    

                except:
                    print('NAO ACHOU ALGO')
                    continue
            
                     
            except:
                print("nao deu")

    arquivo_txt = "web_scraper_restaurantes.txt"
    if not os.path.exists(arquivo_txt):
        with open(arquivo_txt, "w", encoding="utf-8" ) as f:
            f.write(f"{listao}\n")
    else:
        with open(arquivo_txt, "a", encoding="utf-8") as f:
            f.write(f"@%{listao}\n")

                    

