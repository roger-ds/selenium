
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

t = 1
cnpj = '22763502002827'

nav = webdriver.Chrome()
nav.get('https://www.sefaz.ap.gov.br/MATHEUS1/')
nav.find_element(By.NAME, 'login').send_keys('rogerio.rodrigues')
nav.find_element(By.NAME, 'senha').send_keys('Fiscal@960')
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'submit').click()
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'submit').click()
# Mercado
nav.find_element(By.XPATH, '//*[@id="headerwrapper"]/nav/ul/li[7]/a').click()
nav.implicitly_wait(t)
# 4.01 Classifica itens GTIN
nav.find_element(By.XPATH, '//*[@id="headerwrapper"]/nav/ul/li[7]/ul/li[5]/a').click()
nav.implicitly_wait(t)
nav.find_element(By.NAME, 'EMP_CNPJ').send_keys(cnpj)

select_element = nav.find_element(By.NAME,'DATA_INI')
select_object = Select(select_element)
select_object.select_by_value('2021-OUT')
nav.implicitly_wait(t)

select_element = nav.find_element(By.NAME,'DATA_FIM')
select_object = Select(select_element)
select_object.select_by_value('2022-MAR')
nav.implicitly_wait(t)


nav.find_element(By.NAME, 'submit').click()
nav.implicitly_wait(t)
#  temp = nav.find_element(By.ID, 'wob_tm')
#  print(temp.text)
#  nav.quit()
