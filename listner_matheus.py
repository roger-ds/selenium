
# para instanciar o navegador
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# EventFiringWebdriver para disparar os eventos
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.events import AbstractEventListener
from time import sleep
import sys

class MyListener(AbstractEventListener):

    def before_navigate_to(self, url, driver):
        print("Before navigating to ", url)

    def after_navigate_to(self, url, driver):
        print("After navigating to ", url)

    def before_click(self, element, driver):
        if element.tag_name == 'input':
            # print(dir(element))
            # print(driver.find_element(By.TAG_NAME, 'h5').text)
            print("before_click")
            return 'before_click'

    def after_click(self, element, driver):
            print("after_click")


def aguarda_click_do_usuario(element):

    # here is a sample of an element you can create via js (this one is a hidden input)
    javascript = "let element = arguments[0];\
                  element.addEventListener('click', function() { \
                        let input = document.createElement('input'); \
                        input.setAttribute('type', 'hidden');  \
                        input.setAttribute('id', 'my_input'); \
                        document.body.appendChild(input); \
                  });"

    # finally you send the javascript to your webbrowser with execute_script
    ef_firefox.execute_script(javascript,element)

    # then you will be able to wait the element to be created 
    #(30 is te timeout in seconds, you should adjust as you need)
    hiddenInput = WebDriverWait(ef_firefox, 300).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="my_input"]')))

    return hiddenInput


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
input_ = ef_firefox.find_element(By.ID, 'login')

aguarda_click_do_usuario(botao)

input_.click()
