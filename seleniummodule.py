from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time


def abrirpagina (nombrepagina):

    driver = webdriver.Chrome()
    driver.get(nombrepagina)

    # Maximizamos la ventana

    try:
        element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyButtonAccept')))
        driver.execute_script("arguments[0].click();", element)
    except:
        driver.maximize_window()
        # Le damos unos segundos para que cargue. Aplicamos aleatoriedad para emular el comportamiento humano

    time.sleep(2)

    return driver


def descargarbody(driver):


    body = driver.execute_script("return document.body")

    return body


def cerrarpagina():

    driver.quit()
