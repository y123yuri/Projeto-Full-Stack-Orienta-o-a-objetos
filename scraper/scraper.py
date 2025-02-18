import os
import asyncio
import random
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Lista de tipos de culinária para pesquisar no Google
tipos_de_culinaria = [
    "Brasileira", "Italiana", "Japonesa", "Chinesa", "Mexicana",
    "Francesa", "Árabe", "Indiana", "Tailandesa", "Portuguesa"
]

# Caminho do Geckodriver dentro da pasta do projeto
geckodriver_path = os.path.abspath("scraper/geckodriver")

# Configuração do Firefox para evitar detecção
firefox_options = Options()
firefox_options.set_preference("dom.webdriver.enabled", False)
firefox_options.set_preference("useAutomationExtension", False)
firefox_options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/110.0 Safari/537.36"
)
firefox_options.headless = False  # Altere para True se quiser rodar sem interface

# Função assíncrona para rodar o Selenium
async def buscar_no_google(culinaria):
    print(f"\n🔍 Pesquisando: Culinária {culinaria}")

    # Inicia o driver do Firefox
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(service=service, options=firefox_options)

    try:
        # Abrir o Google
        driver.get("https://www.google.com")

        # Encontrar a barra de pesquisa e inserir o termo
        search_box = driver.find_element(By.NAME, "q")
        search_box.clear()
        search_box.send_keys(f"Culinária {culinaria}")
        search_box.send_keys(Keys.RETURN)

        # Espera aleatória para simular comportamento humano
        await asyncio.sleep(random.uniform(2, 5))

        # Capturar os três primeiros resultados
        resultados = driver.find_elements(By.CSS_SELECTOR, "h3")
        print(f"Resultados para 'Culinária {culinaria}':")
        for i, resultado in enumerate(resultados[:3]):
            print(f"{i+1}. {resultado.text}")

    except Exception as e:
        print(f"❌ Erro ao pesquisar {culinaria}: {e}")

    finally:
        driver.quit()

# Função principal assíncrona
async def main():
    tarefas = [buscar_no_google(culinaria) for culinaria in tipos_de_culinaria]
    await asyncio.gather(*tarefas)

# Rodar o script de forma assíncrona
if __name__ == "__main__":
    asyncio.run(main())
