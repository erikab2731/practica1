print("holamundsifrerf")



# Se importan las librerías
from bs4 import BeautifulSoup
# import requests
# import time
# import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import datetime
import time
# Iniciamos el webdriver de chrome y seteamos la página web que vamos a explorar y obtener información
driver = webdriver.Chrome()
driver.get('https://www.exploit-db.com/')
driver.maximize_window()
time.sleep(2)
###############################################################################################################
# Importante. Falta la paginación. Este avance solo es para la primera hoja
###############################################################################################################
# Falta también la regla de carga (un while para las fechas solo de hoy o bien de un id que debemos generar)
###############################################################################################################

# Generamos una regla de espera (15 seg.) para que la página no nos reconozca como robots
# Apuntamos al objeto cuyo id  = 'exploits-table', que es donde está la información que queremos obtener

#try:
#    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'exploits-table')))
#except TimeoutException:
#    pass

body = driver.execute_script("return document.body")
source = body.get_attribute('innerHTML')

#print( "source" + str(source))

cabeceras = BeautifulSoup(source, 'html.parser').find_all('thead')
paginacion = driver.find_element(By.ID, 'exploits-table_paginate')

print( "tablapaginas" + str(paginacion))
print("cabeceras" + str(cabeceras))


cuerpo = BeautifulSoup(source, 'html.parser').find_all('tbody')

print("cuerpo" + str(cuerpo))
# Una vez obtenido el objeto, lo guardamos para poder iterar.
#paginas = driver.find('exploits-table' , { "class" : "table table-striped table-bordered display dataTable no-footer dtr-inline" }).get_attribute('innerHTML')
#print(str(paginas))
# Pasamos el objeto a html y buscamos los atributos que queremos obtener
#html =BeautifulSoup(paginas, 'html.parser')
#cabeceras =BeautifulSoup(paginas, 'html.parser').find_all('tr')

#cuerpo =BeautifulSoup(paginas, 'html.parser').find_all('tbody')




#print(html)
#for th in cabeceras:
#    print( str(th.text))
#print(" cabeceras: " +   str(cabeceras))
#print(" cuerpo: " +   str(cuerpo))



#cerramos la ventana para que chrome no se quede abierto.
driver.quit()
##################################################################################################################
# Falta agregarle los campos de verificación, aplicación vulnerable y quizá la descarga
##################################################################################################################

# Creamos las listas que serán las columnas del dataframe a almacenar
# date_ws = []
# title_ws = []
# type_ws = []
# platform_ws = []
# author_ws = []
#
# for i in range(15):
#     dt = objeto_explorar[8*i].text
#     tt = objeto_explorar[8*i+4].text
#     ty = objeto_explorar[8*i+5].text
#     pt = objeto_explorar[8*i+6].text
#     at = objeto_explorar[8*i+7].text
#     date_ws.append(dt)
#     title_ws.append(tt)
#     type_ws.append(ty)
#     platform_ws.append(pt)
#     author_ws.append(at)
#
# tabla_final = pd.DataFrame({'Date':date_ws,'Title':title_ws,'Type':type_ws,'Platform':platform_ws,'Author':author_ws})
#
# print(tabla_final)
# # Establecemos la fecha para generar el nombre del archivo
# dt_crrt = datetime.datetime.now()
#
# # Guardamos el archivo en un csv
# tabla_final.to_csv('BD_XP_{}_{}_{}_{}_{}_{}.csv'.format(dt_crrt.year,dt_crrt.month,dt_crrt.day,dt_crrt.hour,dt_crrt.minute,dt_crrt.second), index= False,encoding='utf-8-sig')
