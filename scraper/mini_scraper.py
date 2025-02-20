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


link='https://www.google.com/search?q=comida+japonesa+brasilia&client=firefox-b-d&sca_esv=ba1f5db415756174&biw=1366&bih=635&tbm=lcl&ei=DjG3Z-XeEL6J5OUPqviUmAs&ved=0ahUKEwjlnaDCsNKLAxW-BLkGHSo8BbMQ4dUDCAk&uact=5&oq=comida+japonesa+brasilia&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIhhjb21pZGEgamFwb25lc2EgYnJhc2lsaWFIjTtQpA1YoDpwBXgAkAEAmAHzAaABuRqqAQYwLjI2LjG4AQPIAQD4AQGYAhagAo4VwgIFEAAYgATCAgQQABgewgIGEAAYBRgewgIGEAAYFhgewgIMEAAYgAQYQxiKBRgKwgIKEAAYgAQYQxiKBcICCxAAGIAEGLEDGIMBwgIOEAAYgAQYsQMYgwEYigXCAggQABiABBixA8ICBBAAGAPCAgsQABiABBiSAxiKBcICCBAAGIAEGMkDwgIIEAAYgAQYogSYAwCIBgGSBwYxLjIwLjGgB_9Y&sclient=gws-wiz-local#rlfi=hd:;si:10021366631245637726,l,Chhjb21pZGEgamFwb25lc2EgYnJhc2lsaWFI_8ye3K63gIAIWiwQABABGAAYARgCIhhjb21pZGEgamFwb25lc2EgYnJhc2lsaWEqBggDEAAQAZIBE2phcGFuZXNlX3Jlc3RhdXJhbnSaASNDaFpEU1VoTk1HOW5TMFZKUTBGblNVUlljazFYVlZKUkVBRaoBagoIL20vMDJ3Ym0KCC9tLzA0MmNrEAEqEyIPY29taWRhIGphcG9uZXNhKAwyHxABIhvEOqBvO0vW-7TYl_Mq_hnrv5iz7csp3xQcvSgyHBACIhhjb21pZGEgamFwb25lc2EgYnJhc2lsaWH6AQQIABBA,y,gl2FbCH3Jy4;mv:[[-15.737535500000002,-47.8700798],[-15.8430244,-48.0210647]]'
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0"}
requisição=requests.get(link, headers=headers)

options = webdriver.FirefoxOptions()
options.page_load_strategy = 'eager'
# Link de cada professor e matéria
driver = webdriver.Firefox(options=options)

driver.get(link)
time.sleep(5)
html = driver.page_source 
soup= BeautifulSoup(html,"html.parser")

# busca_comentarios = soup.find_all(class_="nNlnIb")
# comentarios = ''
# for falas in busca_comentarios:
#     comentarios_tratamento = falas.get_text()
#     comentarios = comentarios_tratamento

# comentarios = comentarios.replace(comentarios[-28:],'')
# comentarios = comentarios.replace('""', '@')
# comentarios = comentarios.replace('"',"")
# comentarios = comentarios.split("@")

# print('sou os',comentarios)





try:
    botao_descricao = driver.find_element(By.XPATH, '//a[@aria-label="mostrar mais"]')
    time.sleep(3)
    botao_descricao.click()
    print("abri no primeiro")
except:
    try:
        botao_descricao = driver.find_element(By.CLASS_NAME, 'RRYiY')
        time.sleep(3)
        botao_descricao.click()
        print("abri no segundo")

    except:
        print('não achei')
        pass

# horarios = soup.find_all('td', class_='SKNSIb')

# lista_de_horarios = []
# contador_dia = 0
# for horario in horarios:      # dia
#     if contador_dia < 8:
#         dia = horario.get_text(strip=True)
#         proximo_td = horario.find_next('td')
#         horarioo = proximo_td.get_text(strip=True)
#         conjunto = dia+' '+horarioo
#         lista_de_horarios.append(conjunto)
#         contador_dia += 1
#     else:
#         break
#     print(lista_de_horarios)

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