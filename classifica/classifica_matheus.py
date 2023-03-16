
from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from time import sleep
import sys

def iniciar_driver():
    firefox_options = Options()
    arguments = ['--lang=pt-BR', '--width=1200', '--height=750', '--incognito']
    for argument in arguments:
        firefox_options.add_argument(argument)

    driver = webdriver.Firefox(service=FirefoxService(
        GeckoDriverManager().install()), options=firefox_options)

    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait

nav, wait = iniciar_driver()

# Dados
t = 1
cnpj = input('Entre com o CNPJ (apenas números): ')
data_ini = '2022-JUL'
data_fim = '2022-SET'
timeout = 500 # tempo limite em segundos para carregamento da pagina

nav.get('https://www.sefaz.ap.gov.br/MATHEUS1/')
nav.find_element(By.NAME, 'login').send_keys('rogerio.rodrigues')
nav.find_element(By.NAME, 'senha').send_keys('Fiscal#96')
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'submit').click()
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'submit').click()
nav.implicitly_wait(t)

#  Mercado
action = ActionChains(nav)
mercado = nav.find_element(By.XPATH, '//*[@id="headerwrapper"]/nav/ul/li[7]/a')
action.move_to_element(mercado).click().perform()

#  4.01 Classifica itens GTIN
nav.find_element(By.XPATH, '//*[@id="headerwrapper"]/nav/ul/li[7]/ul/li[5]/a').click()
nav.implicitly_wait(t)

#Preenche os dados
nav.find_element(By.NAME, 'EMP_CNPJ').send_keys(cnpj)
select_element = nav.find_element(By.NAME,'DATA_INI')
select_object = Select(select_element)
select_object.select_by_value(data_ini)
nav.implicitly_wait(t)
select_element = nav.find_element(By.NAME,'DATA_FIM')
select_object = Select(select_element)
select_object.select_by_value(data_fim)
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'submit').click()

# Aguarda o carregamento da pagina
try:
    wait.until(lambda nav: nav.execute_script(
        'return document.readyState') == 'complete')
    print('Page is ready!')
except:
    print('Loading took tooo much time')

# Percorre a tabela de itens

try:
    table = nav.find_elements(By.TAG_NAME, 'table')[3]
    body = table.find_elements(By.TAG_NAME, 'tbody')[2]
    rows = body.find_elements(By.TAG_NAME, 'tr')
except:
    print('Não há itens a serem exibidos na tabela')
    sys.exit(0)    

print(str(len(rows)) + ' - linhas')

for i in range(len(rows)):
    columns = rows[i].find_elements(By.TAG_NAME, 'td')
    id_ = i + 2
    
    l = [] 
    values = [] 
    for j in range(len(columns)): 
        l.append(columns[j].text)
    button = columns[4].find_element(By.TAG_NAME, 'button')

    # extrai dados dos campos select
    select_element = nav.find_element(By.ID, 'PRO_' + str(id_))
    select_object = Select(select_element)
    select1 = select_object.first_selected_option.text        

    select_element_div = nav.find_element(By.ID, 'CEST_' + str(id_))
    select_element = select_element_div.find_element(By.TAG_NAME, 'select')
    select_object = Select(select_element)
    select2 = select_object.first_selected_option.text        

    try:
        values.append(l[0])
        values.append(l[1].split('\n')[1])
        values.append(l[2].split('\n')[0][6:13])
        values.append(l[2].split('\n')[1][6:13])
        values.append(l[2].split('\n')[2])
        values.append(l[4].split('\n')[192])
        keys = ['item', 'gtim', 'cest', 'ncm', 'desc', 'cest_sel']
        linha =  dict(zip(keys, values))
        if linha['cest'] == linha['cest_sel'] and select1.startswith("AUTOP"):
            print()
            print('-' * 60)
            print(linha)
            print('Classificacao adotada: ') 
            nav.execute_script(
                'arguments[0].scrollIntoView({block: "center"});', button)
            wait.until(EC.element_to_be_clickable(button))
            button.click()
            nav.implicitly_wait(t)
            print(select1)
            print(select2)

    except IndexError as e:
        print(f'[CLASSIFICAR] linha {i} - {e}')

#nav.quit()
