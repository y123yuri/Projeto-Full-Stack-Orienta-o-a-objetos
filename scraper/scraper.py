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
                pass
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
            if driver.find_element(By.XPATH, xpath):
                time.sleep(3)
                icone_restaurante = driver.find_element(By.XPATH,xpath )  
                icone_restaurante.click()
                time.sleep(8)                                                                       
                html = driver.page_source                                                  
                # Parsear com BeautifulSoup                                                    
                soup = BeautifulSoup(html, "html.parser")                                       
                                                                                                    
                # Buscar os restaurantes
                                                       
                nome_restaurante = soup.find('h2', class_='qrShPb').find_next('span').get_text(strip=True) 
                endereco = soup.find('span', class_='LrzXr').get_text(strip=True) 
                try:
                    telefone = soup.find('span', class_ ='LrzXr zdqRlf kno-fv').find_next('span').get_text(strip=True)
                except:
                    telefone = None
                    
                existencia_botao = False
                try:
                    print('TO NO TRY')
                    time.sleep(3)
                    botao_descricao = driver.find_element(By.XPATH, '//a[@aria-label="mostrar mais"]')
                    existencia_botao = True
                    botao_descricao.click()
                    time.sleep(5)

                    html_2 = driver.page_source 
                    soup_2 = BeautifulSoup(html_2,"html.parser") #esse daqui atualiza a pagina
                    
                    time.sleep(3)

                    descricao_element = soup_2.find('div', attrs={"jsname": "EvNWZc"})
                    descricao = descricao_element.get_text(strip=True)
                    
                    
                except:

                    if existencia_botao == False:
                        try:
                            html_2 = driver.page_source 
                            soup_2 = BeautifulSoup(html_2,"html.parser") #esse daqui atualiza a pagina
                        
                            time.sleep(3)

                            descricao_element = soup_2.find('div', attrs={"jsname": "EvNWZc"})
                            descricao = descricao_element.get_text(strip=True)
                        except:
                            print("esse nao tem descricao")
                            descricao = None
                    else:
                        descricao = None
                        pass
                
                print(nome_restaurante,telefone,descricao)

                # botao_avaliacoes = driver.find_element(By.XPATH,'/html/body/div[2]/div/div[7]/div[2]/div/div[2]/div/div/async-local-kp/div/div/div[1]/div/g-sticky-content-container/div/block-component/div/div[1]/div/div/div/div[1]/div/div/div[5]/div[1]/g-sticky-content/div/div[1]/g-tabs/div/div/a[3]')
                # botao_avaliacoes.click()
                            
            else:
                print("nao deu")
                    





    

