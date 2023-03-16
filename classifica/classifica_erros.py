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
    arguments = ['--lang=pt-BR', '--width=1000', '--height=750', '--incognito']
    for argument in arguments:
        firefox_options.add_argument(argument)

    driver = webdriver.Firefox(service=FirefoxService(
        GeckoDriverManager().install()), options=firefox_options)

    wait = WebDriverWait(
        driver,
        3600, # 1 hora
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait


def aguarda_click_do_usuario(driver, element):

    # here is a sample of an element you can create via js (this one is a hidden input)
    javascript = "let element = arguments[0];\
                  element.addEventListener('click', function() { \
                        let input = document.createElement('input'); \
                        input.setAttribute('type', 'hidden');  \
                        input.setAttribute('id', 'my_input'); \
                        document.body.appendChild(input); \
                  });"

    # finally you send the javascript to your webbrowser with execute_script
    driver.execute_script(javascript,element)

    # then you will be able to wait the element to be created 
    #(30 is te timeout in seconds, you should adjust as you need)
    wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="my_input"]')))

    # remove the element created via js
    element = driver.find_element(By.ID, 'my_input')
    driver.execute_script("""
    var element = arguments[0];
    element.parentNode.removeChild(element);
    """, element)   


# Dados
t = 1
cnpj = input('Entre com o CNPJ (apenas números): ')
data_ini = '2022-JUL'
data_fim = '2022-SET'
timeout = 500 # tempo limite em segundos para carregamento da pagina

nav, wait = iniciar_driver()

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
    print('Loading took toooo much time')

# Percorre a tabela de itens
try:
    table = nav.find_elements(By.TAG_NAME, 'table')[3]
    body = table.find_elements(By.TAG_NAME, 'tbody')[2]
    rows = body.find_elements(By.TAG_NAME, 'tr')
except:
    print('Não há itens a serem exibidos na tabela')
    sys.exit(0)    

print(str(len(rows)) + ' - linhas')
ncm_erro = []
dic_ncm_erro = dict()

for i in range(len(rows)):
    columns = rows[i].find_elements(By.TAG_NAME, 'td')
    id_ = i + 2
    
    l = [] 
    values = [] 
    for j in range(len(columns)): 
        l.append(columns[j].text)
    button = columns[4].find_element(By.TAG_NAME, 'button')

    values.append(l[0])
    values.append(l[1].split('\n')[1])

    if l[2].split('\n')[0][:6] == 'CEST :': 
        values.append(l[2].split('\n')[0][6:13])
        values.append(l[2].split('\n')[1][5:13])
        values.append(l[2].split('\n')[2])
        keys = ['item', 'gtim', 'cest', 'ncm', 'desc']
    else:
        values.append(l[2].split('\n')[0][5:13])
        values.append(l[2].split('\n')[1])
        keys = ['item', 'gtim', 'ncm', 'desc']

    l4 = l[4].split('\n')
    cest_sel = l4.index('CEST') + 1
    if l4[cest_sel] != '':
        values.append(l4[cest_sel])
        keys.append('cest_sel')

    linha =  dict(zip(keys, values))
    print()
    print('-' * 60)
    print(linha)
    print('Classificacao adotada: ') 

    nav.execute_script(
        'arguments[0].scrollIntoView({block: "center"});', button)

    # extrai dados dos campos select
    select_element = nav.find_element(By.ID, 'PRO_' + str(id_))
    select_object = Select(select_element)
    select1 = select_object.first_selected_option.text        

    select_element_div = nav.find_element(By.ID, 'CEST_' + str(id_))
    select_element = select_element_div.find_element(By.TAG_NAME, 'select')
    select_object = Select(select_element)
    select2 = select_object.first_selected_option.text        

    try:
        if linha['cest'] == linha['cest_sel'] and select1 != '':
            button.click()
            nav.implicitly_wait(t)
            print(select1)
            print(select2)
        else:
            1 / 0 # Exception gerada para forćar a entrada  no bloco except

    except Exception as e:
        print(f'[CLASSIFICAR]  linha {i + 1}')

        if linha['ncm'] not in ncm_erro:
            ncm_erro.append(linha['ncm'])
            aguarda_click_do_usuario(nav, button)

            # classifica manualmente  e captrura selecao
            
            select_element = nav.find_element(By.ID, 'PRO_' + str(id_))
            select_object = Select(select_element)
            select1 = select_object.first_selected_option.text        
            print(select1)

            select_element_div = nav.find_element(By.ID, 'CEST_' + str(id_))
            select_element = select_element_div.find_element(By.TAG_NAME, 'select')
            select_object = Select(select_element)
            select2 = select_object.first_selected_option.text        
            print(select2)

            dic_ncm_erro.update({linha['ncm']: [select1, select2]})
        else:

            select_element = nav.find_element(By.ID, 'PRO_' + str(id_))
            select_object = Select(select_element)
            select1 = dic_ncm_erro[linha['ncm']][0]        
            select_object.select_by_visible_text(select1)
            print(select1)
            sleep(t)

            select_element_div = nav.find_element(By.ID, 'CEST_' + str(id_))
            select_element = select_element_div.find_element(By.TAG_NAME, 'select')
            select_object = Select(select_element)
            select2 = dic_ncm_erro[linha['ncm']][1]        
            select_object.select_by_visible_text(select2)
            print(select2)
            sleep(t)

            button.click()
            nav.implicitly_wait(t)
#nav.quit()
