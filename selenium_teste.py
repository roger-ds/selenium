from selenium import webdriver
from selenium.webdriver.common.by import By
import time

nav = webdriver.Chrome()
nav.get('https://www.google.com.br')
nav.find_element(By.NAME, 'q').send_keys('tempo agora')
time.sleep(1)
nav.find_element(By.NAME, 'btnK').click()
temp = nav.find_element(By.ID, 'wob_tm')
print(temp.text)

