import pandas as pd
import datetime
import time
from bs4 import BeautifulSoup
import wget
import random
import time
import re



def iniciardescarga(body):

    source = body.get_attribute('innerHTML')
    cuerpo = BeautifulSoup(source, 'html.parser').find_all('tbody')

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
    n_pre = int(len(cuerpo[indice_body].find_all('i'))/2)

    # Se crea un bucle para asegurar que el número de ítems tomados correspondan a los que muestra el campo "Show" de la
    # página web (ítems mostrados).

    if n_pre < int(list_items_pag[0]):
        print('Hay un error en la cantidad de ítems mostrados')
    elif n_pre < int(list_items_pag[1]):
        n=int(list_items_pag[0])
    elif n_pre < int(list_items_pag[2]):
        n=int(list_items_pag[1])
    elif n_pre < int(list_items_pag[3]):
        n=int(list_items_pag[2])
    else:
        n=int(list_items_pag[3])

    return n, elementos_i, elementos_a, elementos_td



def descargadeitems(n, elementos_i, elementos_a, elementos_td,stored_date):

        id_ws = []
        link_ws = []
        date_ws = []
        verificacion_ws = []
        title_ws = []
        type_ws = []
        platform_ws = []
        author_ws = []
        app_ws = []

        for i in range(n):

            # Obtenemos el link donde especifica el id del registro (formato 'download/<id>'), y lo almacenamos y limpiamos
            # para obtener solo el id numérico
            lnk_dwl = elementos_a[5*i]['href']

            j=0
            while True:
                if not 'load' in lnk_dwl:
                    j += 1
                    lnk_dwl = elementos_a[5*i+j]['href']
                else:
                     break

            id_download = int(re.findall(r'[0-9]+', lnk_dwl)[0])

            date_iter = elementos_td[8*i].text

            # Capturamos los datos mientras que el id capturado sea mayor que el último id almacenado en la bd
            if date_iter >= stored_date:
            #if id_download > last_id_stored:

                # Obtenemos el campo id
                id_r = int(re.findall(r'[0-9]+', elementos_a[5*i+j]['href'])[0])

                # Obtenemos el campo verificación. indica si el exploit fue verificado por Exploit Database
                check_tst = elementos_i[2*i+1]['class'][1]

                if 'mdi-check' in check_tst:
                    chk_r = 'verificado'
                else:
                    chk_r = 'no verificado'


                # Obtenemos el campo aplicación. Indica el link de la aplicación.
                app_tst = elementos_a[5*i+j+1]['href']

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

        tabla_final = pd.DataFrame({'Id':id_ws,'Link Exploit':link_ws, 'App': app_ws, 'Date':date_ws, 'Verification':verificacion_ws,'Title':title_ws,'Type':type_ws,
                                        'Platform':platform_ws,'Author':author_ws})

        return tabla_final
