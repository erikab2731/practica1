from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import seleniummodule
import BSmodule

stored_date = '2018-12-31'

data_exploits = pd.DataFrame(columns=['Id','Link Exploit','App','Date','Verification','Title','Type','Platform','Author'])

primerapagina = True
success = True

while True:
 if primerapagina :
        driver = seleniummodule.abrirpagina('https://www.exploit-db.com/')
        body = seleniummodule.descargarbody(driver)
        n, elementos_i, elementos_a, elementos_td = BSmodule.iniciardescarga(body)
        tabla_final = BSmodule.descargadeitems(n, elementos_i, elementos_a, elementos_td,stored_date)
        primerapagina = False
        if len(tabla_final) == 0:
            driver.quit()
            success = False
            break
        else:
            data_exploits = pd.concat([data_exploits,tabla_final])
 else:
    if len(tabla_final) == 0:
        driver.quit()
        success = False
        break
    else:
        data_exploits = pd.concat([data_exploits,tabla_final])

    max_date = max(tabla_final.Date)

    if stored_date > max_date:
        driver.quit()
        success = False
        break
    else:
        if stored_date == max_date:
            driver.quit()
            break
        else:
            try:
                element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'exploits-table_next')))
                driver.execute_script("arguments[0].click();", element)
                time.sleep(random.uniform(4,7))

                body = seleniummodule.descargarbody(driver)
                n, elementos_i, elementos_a, elementos_td = BSmodule.iniciardescarga(body)
                tabla_final = BSmodule.descargadeitems(n, elementos_i, elementos_a, elementos_td,stored_date)

            except TimeoutException:
                pass


if(success):

    max_xpdb = max(data_exploits['Date'])
    min_xpdb = min(data_exploits['Date'])

    data_exploits.to_csv('exploits_{}{}{}_{}{}{}.csv'.format(min_xpdb[0:4],min_xpdb[5:7],min_xpdb[8:10],max_xpdb[0:4],max_xpdb[5:7],max_xpdb[8:10]), index= False,encoding='utf-8-sig')

else:
    print("Fin del programa")
