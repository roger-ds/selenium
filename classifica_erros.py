from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Dados
t = 1
cnpj = '22763502002827'
data_ini = '2021-OUT'
data_fim = '2022-MAR'
timeout = 500 # tempo limite em segundos para carregamento da pagina

nav = webdriver.Firefox() #Chrome()
nav.get('https://www.sefaz.ap.gov.br/MATHEUS1/')
nav.find_element(By.NAME, 'login').send_keys('rogerio.rodrigues')
nav.find_element(By.NAME, 'senha').send_keys('Fiscal@960')
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
    WebDriverWait(nav, timeout).until(lambda nav: nav.execute_script('return document.readyState') == 'complete')
    print('Page is ready!')
except:
    print('Loading took tooo much time')

# Percorre a tabela de itens

table = nav.find_elements(By.TAG_NAME, 'table')[3]
body = table.find_elements(By.TAG_NAME, 'tbody')[2]
rows = body.find_elements(By.TAG_NAME, 'tr')

print(str(len(rows)) + ' - linhas')
ncm_erro = []
for i in range(len(rows)):
    columns = rows[i].find_elements(By.TAG_NAME, 'td')
    
    l = [] 
    values = [] 
    for j in range(len(columns)): 
        l.append(columns[j].text)
    button = columns[4].find_element(By.TAG_NAME, 'button')

    values.append(l[0])
    values.append(l[1].split('\n')[1])

    if l[2].split('\n')[0][:6] == 'CEST :': 
        values.append(l[2].split('\n')[0][6:13])
        values.append(l[2].split('\n')[1][6:14])
        values.append(l[2].split('\n')[2])
        keys = ['item', 'gtim', 'cest', 'ncm', 'desc']#, 'cest_sel']

    values.append(l[2].split('\n')[0][6:14])
    values.append(l[2].split('\n')[1])
    keys = ['item', 'gtim', 'ncm', 'desc']

    l4 = l[4].split('\n')
    if 'CEST' in l4:
        cest_sel = l4.index('CEST') + 1
        values.append(cest_sel)
        keys.append('cest_sel')

    linha =  dict(zip(keys, values))

    try:
        if linha['cest'] == linha['cest_sel']:
            print(linha)
            button.click()
            nav.implicitly_wait(t)

    except IndexError as e:
        print(f'[ERRO] na linha {i} - {e}')
        ncm_erro.append(linha['ncm'])
        autopecas = input( 'Sugestao de Classificacao: ')






#nav.quit()
