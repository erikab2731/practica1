# Se importan las librerías
from bs4 import BeautifulSoup
import wget
import random
import time
import re
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
#options = webdriver.ChromeOptions()
#options.add_argument("user-data-dir= C:\\Users\\erika\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
#driver = webdriver.Chrome(executable_path="C:\\Users\\erika\\Documents\\MASTER\\TIPOLOGÍA Y CICLO DE VIDA DE LOS DATOS\\practica1\\practica1\\chromedriver.exe", options=options)
driver.get('https://www.exploit-db.com/')
# Maximizamos la ventana
#driver.execute_script("javascript: void(0);")
try:
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyButtonAccept')))
    driver.execute_script("arguments[0].click();", element)
except:
    driver.maximize_window()
# Le damos unos segundos para que cargue. Aplicamos aleatoriedad para emular el comportamiento humano
time.sleep(2)

#time.sleep(random.uniform(2,3))

# Obtenemos el último archivo guardado, según id. Esto podría ser una consulta sobre alguna bd donde se almacenen
# los archivos scrapeados
last_id_stored = 48222 # 47700

stored_date = '2018-12-31'

data_exploits = pd.DataFrame(columns=['Id','Link Exploit','App','Date','Verification','Title','Type','Platform','Author'])

# Ejecutamos una rutina hasta que se haya obtenido todos los id mayores o iguales a 'last_id_stored'
while True:

    # Obtenemos el cuerpo del html
    body = driver.execute_script("return document.body")
    source = body.get_attribute('innerHTML')
    cuerpo = BeautifulSoup(source, 'html.parser').find_all('tbody')
    print (str(cuerpo))
    
    if len(cuerpo)<4:
        indice_body = 0
    else:
        indice_body = 5
    
    # Capturamos los elementos td: date, title, type, platform y author
    elementos_td = cuerpo[indice_body].find_all('td')

    # Capturamos los elementos a: id
    elementos_a = cuerpo[indice_body].find_all('a', href=True)

    # Capturamos los elementos i: verificación
    elementos_i = cuerpo[indice_body].find_all('i')

    # Establecemos la cantidad de registros a capturar en el cuerpo.
    # Cantidad de ítems a mostrar 
    items_pag = BeautifulSoup(source, 'html.parser').find_all(True, {'class':'dataTables_length'})[0].find_all('option')
    list_items_pag = []
    for i in range(len(items_pag)):
        lip = items_pag[i].text
        list_items_pag.append(lip)
    
    # Calculamos la cantidad de elementos i y lo dividimos entre 2 para aproximar la cantidad de ítems mostrados
    n_pre = int(len(cuerpo[0].find_all('i'))/2)
    
    # Se crea un bucle para asegurar que el número de ítems tomados correspondan a los que muestra el campo "Show" de la 
    # página web (ítems mostrados).
    
    if n_pre < int(list_items_pag[0]):
        print('Hay un error en la cantidad de ítems mostrados')
        driver.quit()
        break
    elif n_pre < int(list_items_pag[1]):
        n=int(list_items_pag[0])
    elif n_pre < int(list_items_pag[2]):
        n=int(list_items_pag[1])
    elif n_pre < int(list_items_pag[3]):
        n=int(list_items_pag[2])
    else:
        n=int(list_items_pag[3])
        
    #n = 15

    # Creamos las listas donde almacenaremos los valores capturados
    id_ws = []
    link_ws = []
    date_ws = []
    verificacion_ws = []
    title_ws = []
    type_ws = []
    platform_ws = []
    author_ws = []
    app_ws = []
    # Generamos el bucle para capturar cada campo de interés y lo almacenaremos en un dataframe
    for i in range(n):

        # Obtenemos el link donde especifica el id del registro (formato 'download/<id>'), y lo almacenamos y limpiamos
        # para obtener solo el id numérico
        lnk_dwl = cuerpo[indice_body].find_all('a', href=True)[5*i]['href']

        #lnk_dwl = cuerpo[0].find_all('a', href = True)[0]['href']
        print(str(lnk_dwl))
        j=0
        while True:
            if not 'load' in lnk_dwl:
                j += 1
                lnk_dwl = cuerpo[indice_body].find_all('a', href=True)[5*i+j]['href']
            else:
                 break

        id_download = int(re.findall(r'[0-9]+', lnk_dwl)[0])
        
        date_iter = elementos_td[8*i].text

        # Capturamos los datos mientras que el id capturado sea mayor que el último id almacenado en la bd
        if date_iter>=stored_date:
        #if id_download > last_id_stored:

            # Obtenemos el campo id
            id_r = int(re.findall(r'[0-9]+', elementos_a[5*i+j]['href'])[0])

            # Obtenemos el campo verificación. indica si el exploit fue verificado por Exploit Database
            check_tst = elementos_i[2*i+1]['class'][1]

            if 'mdi-check' in check_tst:
                chk_r = 'verificado'
            else:
                chk_r = 'no verificado'

#             app_tst = elementos_i[2*i+1]['class'][2]
#             print(str(app_tst))
#             if app_tst is None:
#                 app_r = ''
#             else:
#                 app_r = 'https://www.exploit-db.com'+ cuerpo[indice_body].find_all('a', href=True)[5*i]['href']

#             print(str(app_r))
            
            # Obtenemos el campo aplicación. Indica el link de la aplicación.
            app_tst = cuerpo[indice_body].find_all('a', href=True)[5*i+j+1]['href']
        
            # Obtenemos el campo aplicación
            if 'exploit' in app_tst:
                app_r = ''
            else:
                app_r = 'https://www.exploit-db.com'+app_tst
            
            date_r = elementos_td[8*i].text # Obtenemos el campo fecha
            title_r = elementos_td[8*i+4].text # Obtenemos el campo título
            type_r = elementos_td[8*i+5].text # Obtenemos el campo tipo
            platf_r = elementos_td[8*i+6].text # Obtenemos el campo plataforma
            author_r = elementos_td[8*i+7].text # Obtenemos el campo autor

            # Adjuntamos el valor de los campos a sus respectivas listas
            verificacion_ws.append(chk_r)
            id_ws.append(id_r)
            date_ws.append(date_r)
            title_ws.append(title_r)
            type_ws.append(type_r)
            platform_ws.append(platf_r)
            author_ws.append(author_r)
            app_ws.append(app_r)
            # Descargamos el archivo del código (.py, .txt, .pdf, etc.) en la carpeta especificada
            url = 'https://www.exploit-db.com'+lnk_dwl
            link_ws.append(url)
            ###########################
            # Importante: Setear la carpeta donde se descargarán los archivos
            ###########################
        #    wget.download(url,out='C:\\Users\\erika\\Documents\\MASTER\\TIPOLOGÍA Y CICLO DE VIDA DE LOS DATOS\\practica1')
        else:
            pass

    # Generamos un dataframe donde almacenamos las listas (columnas) de los campos obtenidos
    tabla_final = pd.DataFrame({'Id':id_ws,'Link Exploit':link_ws, 'App': app_ws, 'Date':date_ws, 'Verification':verificacion_ws,'Title':title_ws,'Type':type_ws,
                                'Platform':platform_ws,'Author':author_ws})

    # Verificamos si la lista de id está vacía. Si lo está, terminamos el bucle y cerramos el driver.
    # En caso no esté vacía, concatenamos la data almacenada de la página al dataframe que creamos al inicio
    if id_ws:

        data_exploits = pd.concat([data_exploits,tabla_final])

    else:
        driver.quit()
        break

    min_id = min(id_ws)
    # Para la paginación, verificamos si el último id almacenado en bd es mayor que el mínimo id capturado.
    # En caso no se cumpla, se pasa a la siguiente página
    if last_id_stored > min_id:
        driver.quit()
        break
    else:
        try:
            element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'exploits-table_next')))
            driver.execute_script("arguments[0].click();", element)
            time.sleep(random.uniform(4,7))
        except TimeoutException:
            pass

###########################
# Opcional
###########################
# Establecemos la fecha para generar el nombre del archivo
# dt_crrt = datetime.datetime.now()
###########################

# Calculamos el máximo y mínimo de las fechas para generar el nombre del archivo, y lo guardamos.
max_xpdb = max(data_exploits['Date'])
min_xpdb = min(data_exploits['Date'])

data_exploits.to_csv('exploits_{}{}{}_{}{}{}.csv'.format(min_xpdb[0:4],min_xpdb[5:7],min_xpdb[8:10],max_xpdb[0:4],max_xpdb[5:7],max_xpdb[8:10]), index= False,encoding='utf-8-sig')

###########################
# Opcional nombre archivo guardado
###########################
# Guardamos el archivo en un csv con el formato del nombre:
# '<max_id><min_id><año><mes><dia><hora><minuto>_<segundo>'

#data_exploits.to_csv('{}{}{}{}{}{}{}_{}.csv'.format(max_xpdb,minxpdb,dt_crrt.year,dt_crrt.month,dt_crrt.day,dt_crrt.hour,dt_crrt.minute,dt_crrt.second), index= False,encoding='utf-8-sig')
