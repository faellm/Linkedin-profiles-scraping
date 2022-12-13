# Importando as bibliotecas
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from PySimpleGUI import PySimpleGUI as sg
from time import sleep
import csv
from data import *
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
    driver = webdriver.Chrome('/Users/rafaellaramartins/Desktop/99freelas/chromedriver - cópia', chrome_options=options)
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

    sleep(3)

    senha = driver.find_element(By.ID, input_pass)
    senha.send_keys(password)

    buttun_entrar= driver. find_element(By.CLASS_NAME, btn_entrar)
    sleep(1)
    buttun_entrar.click()
    sleep(5)
    
    
    
    # GIT
    '''
    email_field = driver.find_element(By.ID, ('username'))
    email_field.send_keys(username)
    print('- insiriu o email')
    sleep(3)

    password_field = driver.find_element(By.ID, ('password'))
    password_field.send_keys(password)
    print('- Insiriu a senha')
    sleep(2)

    # Epata 1.2: Clicando no botão 'entrar'
    buttun_entrar= driver. find_element(By.CLASS_NAME, ('btn__primary--large from__button--floating'))
    buttun_entrar.click()
    sleep(3)
    '''

    print('- Etapa 1 : Concluida')

    # Etapa 2: Indo para a pagina com todas as pessoas da área
    # Etapa 2.1: Formatando URL para direcionar
    url_people = f'https://www.linkedin.com/search/results/people/?keywords={input_profissional}'
    driver.get(url_people)

# Etapa 3: Scraping das URL dos perfils
# Etapa 3.1: Função para extrair a url de uma pagina
    def GetURL():
        '''
          #ME
        page_source = BeautifulSoup(driver.page_source, features="lxml")
        
        #div com o produto
        #profiles = page_source.findAll('div', attrs={'class': 'entity-result__item'})
        #selecionando o link em uma variavel(link)
        links = page_source.find_all('a', attrs={'class':'app-aware-link  scale-down '})
        for link in links:
                     
            print('Link do perfil:',link['href'])
                
            print('\n\n')
        
        '''
      
        #GIT
        
        page_source = BeautifulSoup(driver.page_source)
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
    for page in range(input_page):
        URLs_one_page = GetURL()
        sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);') #scroll to the end of the page
        sleep(3)
        
        # Botão para ir na proxima pagina.
        next_button = driver.find_element(By.XPATH('//*[@id="ember103"]'))
        next_button.click()
        
        URLs_all_page = URLs_all_page + URLs_one_page
        sleep(2)

    print('- Etapa 3: Coletando as URLs')


    # Task 4: Obtendo os dados de um perfik e escrevendo no .CSV
    
    with open('output.csv', 'w',  newline = '') as file_output:
        headers = ['Name', 'Job Title', 'Location', 'URL']
        writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
        writer.writeheader()
        
        for linkedin_URL in URLs_all_page:
            driver.get(linkedin_URL)
            print('- Accessing profile: ', linkedin_URL)
            sleep(3)
            page_source = BeautifulSoup(driver.page_source, "html.parser")
            info_div = page_source.find('div',{'class':'ph5 pb5'})
            try:
                name = info_div.find('h1', class_='text-heading-xlarge inline t-24 v-align-middle break-words').get_text().strip() #Remove unnecessary characters 
                print('--- Profile name is: ', name)
                location = info_div.find('li', class_='t-16 t-black t-normal inline-block').get_text().strip() #Remove unnecessary characters 
                print('--- Profile location is: ', location)
                title = info_div.find('h2', class_='mt1 t-18 t-black t-normal break-words').get_text().strip()
                print('--- Profile title is: ', title)
                writer.writerow({headers[0]:name, headers[1]:location, headers[2]:title, headers[3]:linkedin_URL})
                print('\n')
            except:
                
                break

    print('Mission Completed!')

#Ler os eventos do front end
while True:
    
    
    eventos, valores = window.read()
    #var do input do Layout
    input_profissional = (eventos,valores[0])
    # input de quantas paginas
    input_page = 5  
    print(eventos, valores)
    #input_page = (eventos, valores[5])  
    
    if eventos == sg.WINDOW_CLOSED:
        
        print('fechando...')
        break
        
    
    if eventos == 'Pesquisar':
        Exec()
        print('tudo correto.')
        break