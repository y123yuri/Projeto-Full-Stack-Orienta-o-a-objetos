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
for comida in tipos_comida:

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
            print("nao enconteri")
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
            if driver.find_element(By.XPATH,xpath):
                
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
                    
                    endereco = soup.find('span', class_='LrzXr').get_text(strip=True) 
                
                    telefone = soup.find('span', class_ ='LrzXr zdqRlf kno-fv').find_next('span').get_text(strip=True)

                    
                    time.sleep(3)
                    try:
                        botao_descricao = driver.find_element(By.XPATH, '//a[@aria-label="mostrar mais"]')
                        time.sleep(3)
                        botao_descricao.click()
                    except:
                        try:
                            botao_descricao = driver.find_element(By.XPATH, '//a[@aria-label="mostrar mais"]')
                            time.sleep(3)
                            botao_descricao.click()
                        except:
                            continue

                    time.sleep(5)
                    print('abri a descricao')

                    html = driver.page_source 
                    soup= BeautifulSoup(html,"html.parser") #esse daqui atualiza a pagina
                    
                    time.sleep(3)

                    descricao_element = soup.find('div', attrs={"jsname": "EvNWZc"})
                    descricao = descricao_element.get_text(strip=True)
                    print(f'essa e a descricao {descricao}')

                    
                    time.sleep(3)
                    html = driver.page_source 
                    soup= BeautifulSoup(html,"html.parser") #esse daqui atualiza a pagina


                    horarios = soup.find_all('td', class_='SKNSIb')

                    for horario in horarios:
                        print(horario.get_text(strip=True))
                        proximo_td = horario.find_next('td')
                        if proximo_td:
                            print(proximo_td.get_text(strip=True))    
                    

                    numero_avaliacao = soup.find('span', class_='fzTgPe Aq14fc').get_text(strip=True)
                    print(numero_avaliacao)


                    fotos1 = soup.find_all('div', class_='vwrQge')
                   
                    
                    fotos = f'{fotos1}'

                    fotos = fotos.replace('<',"")
                    fotos = fotos.replace('>',"")

                    fotos = fotos.split(",")
                    
                    for url in fotos:
                        pos1 = url.find('(')
                        pos2 = url.find(")")
                        link = url[pos1 + 1:pos2]
                        print(link)


                    # comentario_avalicao = soup.find_all('a', class_='a-no-hover-decoration').get_text(strip=True)
                    # print(comentario_avalicao)
                        
                    time.sleep(3)
                    
                    links = driver.find_elements(By.CLASS_NAME, 'PbOY2e')
                    # nomes_span = soup.find_all('span', class_='PbOY2e').get_text(strip=True)

                    

                    if len(links) == 4:
                        time.sleep(3)
                        links[1].click()
                    elif len(links) == 5:
                        time.sleep(3)
                        link[2].click()
                    elif len(links) == 3:
                        time.sleep(3)
                        link[0].click()
                    elif len(links) == 6:
                        time.sleep(3)
                        link[3].click()
                    elif len(links) == 7:
                        time.sleep(3)
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
                    time.sleep(3)
                    


                except:
                    print('NAO ACHOU ALGO')
                    continue
                    

                    
                
                
                            
            else:
                print("nao deu")
                    

