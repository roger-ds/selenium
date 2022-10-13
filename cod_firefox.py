from selenium.common.exceptions import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def iniciar_driver():
    firefox_options = Options()
    arguments = ['--lang=pt-BR', '--width=800', '--height=900', '--incognito']
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

driver, wait = iniciar_driver()

input('')
driver.close()
