# Importando as bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from PySimpleGUI import PySimpleGUI as sg
from time import sleep
import csv
from openpyxl import Workbook, load_workbook
from data import *
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
print('- Importou todas as bibliotecas')

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument( 'options.add_argument( window-size=1200 x 600 )' )

# Etapa 1: Login no Linkedin e interface

#  Definindo tema
sg.theme('Reddit')
layout = [
    [sg.Text('Pesquisa ')],
    [sg.Input()],
    [sg.Button('Buscar')]
]

#Justando janela do PySimpleGUI
window = sg.Window('Linkedin Scraping', layout)

# Etapa 1.2: Inserindo o usuario e senha
def Exec():
    # Etapa 1.1: Abrindo o navegador e acessando a pagina de login do Linkedin
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=options)
    sleep(2)
    url = 'https://www.linkedin.com'
    driver.get(url)
    print('- Iniciou o Chrome')
    sleep(2)

    # Etapa 1.2: Importando o usuario e a senha
    credential = open('credentials.txt')
    line = credential.readlines()
    username = line[0]
    password = line[1]
    print('- Importou as credenciais')
    sleep(2)
    # meu
    
    entrar = driver.find_element(By.ID, input_user)
    entrar.send_keys(username)

    sleep(4)

    senha = driver.find_element(By.ID, input_pass)
    senha.send_keys(password)

    buttun_entrar= driver. find_element(By.CLASS_NAME, btn_entrar)
    sleep(2)
    buttun_entrar.click()
    sleep(5)
    
    try:
        btn_captch = driver.find_element(By.ID, 'home_children_button')
        print('favor resolver captcha.')
        for i in range(0,60):
            print('60 segundos para realizar o captcha')
            print('Time:', i)
    except:
        pass
    print('- Etapa 1 : Concluida')

    # Etapa 2: Indo para a pagina com todas as pessoas da área
    # Etapa 2.1: Formatando URL para direcionar
    url_people = f'https://www.linkedin.com/search/results/people/?keywords={input_profissional}'
    driver.get(url_people)

# Etapa 3: Scraping das URL dos perfils
# Etapa 3.1: Função para extrair a url de uma pagina
    def GetURL():

        page_source = BeautifulSoup(driver.page_source, features="lxml")
        profiles = page_source.find_all('a', class_ = 'app-aware-link') 
        #('a', class_ = 'search-result__result-link ember-view')
        all_profile_URL = []
        for profile in profiles:
            profile_ID = profile.get('href')
            profile_URL = "https://www.linkedin.com" + profile_ID
            profile_URL = profile.get('href')
            if profile_URL not in all_profile_URL:
                all_profile_URL.append(profile_URL)
            
        return all_profile_URL
        
    GetURL()
    
    # Etapa 3.2: Navegando sobre as paginas e obtendo as URLs
    URLs_all_page = []

    for page in range(0,6):
        
        URLs_one_page = GetURL()
        sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
        sleep(3)
        
        # Botão para ir na proxima pagina.
        #next_button = driver.find_element(By.XPATH('//*[@id="ember103"]'))
        #next_button.click()
        
        URLs_all_page = URLs_all_page + URLs_one_page
        sleep(3)

    print('- Etapa 3: Coletando as URLs')

    
    # Task 4: Obtendo os dados de um perfik e escrevendo no .CSV
    

        
    for linkedin_URL in URLs_all_page:
            
        driver.get(linkedin_URL)
        sleep(3)
        print('---------------------------------------')
        print('- Link: ', linkedin_URL)
        sleep(3)
        page_source = BeautifulSoup(driver.page_source, "html.parser")
        info_div = page_source.find('div',{'class':'ph5 pb5'})
        try:
            nome = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Profile name is: ', nome)
            location = info_div.find('span', class_='text-body-small inline t-black--light break-words').get_text().strip() #Remove unnecessary characters 
            print('--- Localização: ', location)
            title = info_div.find('li', class_='pv-text-details__right-panel-item').get_text().strip()
            print('--- Titulo: ', title)
            #Contatos
            btn_informacao = driver.find_element(By.ID, 'top-card-text-details-contact-info').click()
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            pop_up = page_source.find('div', class_='pv-profile-section__section-info section-info')
            fone = pop_up.find('ul', class_='list-style-none').get_text().strip()
            print(fone)
            email = pop_up.find('a', class_='pv-contact-info__contact-link link-without-visited-state t-14').get_text().strip()
            print(email)
            instantania = pop_up.find('ul', class_='list-style-none').get_text().strip()
            print(instantania)
            sleep(1)
            
            
            
            with open('recrutamento.csv', 'w',  newline = '') as file_output:
                headers = ['Name','Job Title','Location', 'URL', 'Telefone', 'Email']
                writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
                writer.writeheader()
                writer.writerow({headers[1]:nome, headers[2]:title, headers[3]:location, headers[4]:linkedin_URL, headers[5]:fone, headers[6]:email})
                print('\n')
                print('---------------------------------------')
        except:
            pass  
                     
        
            
                

    print('Mission Completed!')

#Ler os eventos do front end
while True:
    
    
    eventos, valores = window.read()
    #var do input do Layout
    input_profissional = (valores[0])
    # input de quantas paginas
    input_page = 1  
    print(valores[0])
    #input_page = (eventos, valores[5])  
    
    if eventos == sg.WINDOW_CLOSED:
        
        print('fechando...')
        break
        
    
    if eventos == 'Buscar':
        Exec()
        print('tudo correto.')
        break