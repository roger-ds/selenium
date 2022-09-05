
# para instanciar o navegador
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# EventFiringWebdriver para disparar os eventos
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from time import sleep

class MyListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        print("Before navigating to ", url)

    def after_navigate_to(self, url, driver):
        print("After navigating to ", url)

    def before_click(self, element, driver):
        print("before_click")
        e = driver.switch_to.active_element
        return e
    def after_click(self, element, driver):
        print("after_click")


firefox = webdriver.Firefox()
listener = MyListener()

# Dados
t = 1

# Firefox com os eventos sendo disparados
ef_firefox = EventFiringWebDriver(firefox, listener)

ef_firefox.get('https://www.sefaz.ap.gov.br/MATHEUS1/')

ef_firefox.find_element(By.NAME, 'login').send_keys('rogerio.rodrigues')
ef_firefox.find_element(By.NAME, 'senha').send_keys('Fiscal@960')
#  ef_firefox.implicitly_wait(t)
#  ef_firefox.find_element(By.NAME, 'submit').click()
#  ef_firefox.implicitly_wait(t)
botao = ef_firefox.find_element(By.NAME, 'submit')
#botao.click()
    
sleep(10)

elemento = listener.before_click(botao, ef_firefox)

print(elemento.text)

