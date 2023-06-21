import requests
import threading
import gc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import itertools as iter
import re
import threading
import numpy as np
from multiprocessing.pool import ThreadPool
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

import warnings
import sys
warnings.filterwarnings("ignore")


TOKEN = "5717884327:AAG1XYqDvCJMB1cpE3PlnjipwZv2rzOS8ns"
chat_id = "-1001695455818"
message=""
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

endpoint = 'https://www.flashscore.sk/'
CPU_COUNT = 4
checknute_zapasy = {}

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--start-fullscreen')
#chrome_options.add_argument('--disable-dev-shm-usage')

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        self.driver.quit() # clean up driver when we are cleaned up
        print('The driver has been "quitted".')

    @classmethod
    def create_driver(cls):
        the_driver = getattr(threadLocal, 'the_driver', None)
        if the_driver is None:
            #print('Creating new driver.')
            the_driver = cls()
            threadLocal.the_driver = the_driver
        driver = the_driver.driver
        the_driver = None
        return driver

def max_from_onextwo(row,column):
    max_jednotka = row[row.jednotka==row.jednotka.max()].head(1)
    max_x = row[row.x==row.x.max()].head(1)
    max_dvojka = row[row.dvojka==row.dvojka.max()].head(1)
    if(column=='jednotka'):
        return max_jednotka[['stranka','jednotka']]
    elif(column=='x'):
        return max_x[['stranka','x']]
    return max_dvojka[['stranka','dvojka']]

def check_multithread(zapasy_id):
    try:
        if(checknute_zapasy[zapasy_id]==1):
            pass
    except Exception as e:
        checknute_zapasy[zapasy_id]=1
    berem = ['1X2','HOME/AWAY','O/U','AH','DŠ']
    try:
        driver_zapas = Driver.create_driver()
        #driver_zapas = webdriver.Chrome(options=chrome_options)
        driver_zapas.get(zapasy_id)
    except:
        pass
    try:
        number = 6
        while True:
            try:
                tabs = driver_zapas.find_element_by_xpath(f"//*[@id='detail']/div[{number}]/div[1]/div")
                #print(f'zapas {zapasy_id} number {number}')
                break
            except Exception as e:
                number = number + 1
        tabs = driver_zapas.find_element_by_xpath(f"//*[@id='detail']/div[{number}]/div[1]/div")
        tabs_inside = []
        [tabs_inside.append(tab) for tab in tabs.find_elements_by_class_name('tabs__tab') if(tab.text in berem)]
        ds_pandas = pd.DataFrame()
        onextwo_pandas = pd.DataFrame()
        home_away_pandas= pd.DataFrame()
        ou_pandas = pd.DataFrame()
        ah_pandas = pd.DataFrame()
        for tab in tabs_inside:
            if "selected" not in tab.get_attribute('class'):
                WebDriverWait(driver_zapas, 20).until(EC.element_to_be_clickable(tab))
                driver_zapas.execute_script("arguments[0].click();", tab)
            sety = tab.find_elements_by_xpath(f"//*[@id='detail']/div[{number}]/div[2]")
            for sett in sety:
                sett_linky = sett.find_elements_by_class_name('subTabs__tab')
                for set_link in sett_linky:
                    if "selected" not in set_link.get_attribute('class'):
                        WebDriverWait(driver_zapas, 20).until(EC.element_to_be_clickable(set_link))
                        driver_zapas.execute_script("arguments[0].click();", set_link)
                    wrapper = driver_zapas.find_element_by_xpath(f"//*[@id='detail']/div[{number}]/div[3]")
                    tabulky = wrapper.find_elements_by_class_name('ui-table__body')
                    for tabulka in tabulky:
                        riadky = tabulka.find_elements_by_class_name('ui-table__row')
                        for riadok in riadky:
                            vsetko = {}
                            vymazane_kurzy = []
                            try:
                                #print(riadok.find_elements_by_class_name('oddsCell__odd').get_attribute('title'))
                                [vymazane_kurzy.append(x.text) for counter,x in enumerate(riadok.find_elements_by_class_name('oddsCell__odd')) if "Kurzy odstránené bookmakerom" in x.get_attribute('title')]
                            except Exception as e:
                                pass
                            vsetko['set'] = set_link.text
                            vsetko['stranka'] = riadok.find_element_by_class_name('prematchLink').get_attribute('title')
                            kurzy = riadok.text.split('\n')
                            for x in vymazane_kurzy:
                                kurzy[kurzy.index(x)]='-'
                            if(tab.text=='HOME/AWAY'):
                                vsetko['jednotka']=kurzy[0]
                                vsetko['dvojka']=kurzy[1]
                                home_away_pandas = home_away_pandas.append(vsetko, ignore_index=True)
                            elif(tab.text=='O/U'):
                                vsetko['gemy']=kurzy[0]
                                vsetko['over']=kurzy[1]
                                vsetko['under']=kurzy[2]
                                ou_pandas = ou_pandas.append(vsetko, ignore_index=True)
                            elif(tab.text=='AH'):
                                vsetko['gemy']=kurzy[0]
                                vsetko['jednotka_gemy']=kurzy[1]
                                vsetko['dvojka_gemy']=kurzy[2]
                                ah_pandas = ah_pandas.append(vsetko, ignore_index=True)
                            elif(tab.text=='DŠ'):
                                vsetko['jednotkax']=kurzy[0]
                                vsetko['jednadva']=kurzy[1]
                                vsetko['xdva']=kurzy[2]
                                ds_pandas = ds_pandas.append(vsetko, ignore_index=True)
                            elif(tab.text=='1X2'):
                                vsetko['jednotka']=kurzy[0]
                                vsetko['x']=kurzy[1]
                                vsetko['dvojka']=kurzy[2]
                                onextwo_pandas = onextwo_pandas.append(vsetko, ignore_index=True)

        try:
            home_away_pandas.loc[home_away_pandas.jednotka=='-',"jednotka"]=1.00
            home_away_pandas.loc[home_away_pandas.dvojka=='-',"dvojka"]=1.00
            home_away_pandas[home_away_pandas.columns.difference(['set', 'stranka'])] = home_away_pandas[home_away_pandas.columns.difference(['set', 'stranka'])].astype(float)
            home_away_pandas.set = home_away_pandas.set.str.replace(r'\([0-9]*\)','',regex=True)
            home_away_pandas = home_away_pandas[home_away_pandas.stranka!='Unibet']
            home_away_pandas = home_away_pandas[home_away_pandas.stranka!='bet365']
            for home_away_set in home_away_pandas.set.unique():
                for home_away_jednotka in home_away_pandas.loc[home_away_pandas.set==home_away_set].iterrows():
                    for home_away_dvojka in home_away_pandas.loc[home_away_pandas.set==home_away_set].iterrows():
                        # home_away_pandas[f'HOME AWAY - {home_away_set} | JEDNOTKA : {home_away_jednotka[1].stranka} - {home_away_jednotka[1].jednotka} | DVOJKA : {home_away_dvojka[1].stranka} - {home_away_dvojka[1].dvojka}'] = pow(float(home_away_jednotka[1].jednotka),-1)  + pow(float(home_away_dvojka[1].dvojka),-1)
                        home_away_pandas[f'HOME AWAY - {home_away_set} | JEDNOTKA : {home_away_jednotka[1].stranka} - {home_away_jednotka[1].jednotka} | DVOJKA : {home_away_dvojka[1].stranka} - {home_away_dvojka[1].dvojka}'] = ((100 / (home_away_jednotka[1].jednotka/home_away_dvojka[1].dvojka + 1))*home_away_jednotka[1].jednotka)-100
            home_away_results_first_col = home_away_pandas.transpose().columns[0]
            home_away_results = home_away_pandas.transpose()[home_away_results_first_col].drop(['set','stranka','jednotka','dvojka'])
            max_home_away = home_away_results.sort_values(ascending=False).head(1)
        except Exception as e:
            max_home_away=pd.DataFrame([0])[0]
            #print(max_home_away)
            print(f'Daco zle v Home away. Skip. ID : {zapasy_id} , {e}')
            pass
        ##################################################################################################
        try:
            ou_pandas.loc[ou_pandas.over=='-',"over"]=1.00
            ou_pandas.loc[ou_pandas.under=='-',"under"]=1.00
            ou_pandas[ou_pandas.columns.difference(['set', 'stranka'])] = ou_pandas[ou_pandas.columns.difference(['set', 'stranka'])].astype(float)
            ou_pandas.set = ou_pandas.set.str.replace(r'\([0-9]*\)','',regex=True)
            ou_pandas = ou_pandas[ou_pandas.stranka!='Unibet']
            ou_pandas = ou_pandas[ou_pandas.stranka!='bet365']
            for ou_set in ou_pandas.set.unique():
                for gem in ou_pandas.gemy.unique():
                    for over in ou_pandas.loc[(ou_pandas.set==ou_set)&(ou_pandas.gemy==gem)].iterrows():
                        for under in ou_pandas.loc[(ou_pandas.set==ou_set)&(ou_pandas.gemy==gem)].iterrows():        
                            #print(f'set {ou_set} gem {gem} over {over[1].over} under {under[1].under}')
                            # ou_pandas[f'O/U - {ou_set} | CELKOM : {gem} | OVER : {over[1].stranka} - {over[1].over} | UNDER : {under[1].stranka} - {under[1].under}'] = pow(over[1].over,-1) + pow(under[1].under,-1)
                            ou_pandas[f'O/U - {ou_set} | CELKOM : {gem} | OVER : {over[1].stranka} - {over[1].over} | UNDER : {under[1].stranka} - {under[1].under}'] = ((100 / (over[1].over/under[1].under + 1))*over[1].over)-100
            ou_pandas_first_col = ou_pandas.transpose().columns[0]
            ou_pandas_results = ou_pandas.transpose()[ou_pandas_first_col].drop(['set','stranka','gemy','over','under'])
            max_ou_pandas = ou_pandas_results.sort_values(ascending=False).head(1)

        except Exception as e:
            max_ou_pandas=pd.DataFrame([0])[0]
            #print(max_ou_pandas)
            print(f'Daco zle v O/U. Skip. ID: {zapasy_id}, {e}')
            pass
        #################################################################################################
        try:
            ah_pandas.loc[ah_pandas.jednotka_gemy=='-',"jednotka_gemy"]=1.00
            ah_pandas.loc[ah_pandas.dvojka_gemy=='-',"dvojka_gemy"]=1.00
            ah_pandas['gemy'] = pd.to_numeric(ah_pandas['gemy'], errors='coerce')
            ah_pandas = ah_pandas.dropna(subset=['gemy'])
            ah_pandas[ah_pandas.columns.difference(['set', 'stranka'])] = ah_pandas[ah_pandas.columns.difference(['set', 'stranka'])].astype(float)
            ah_pandas.set = ah_pandas.set.str.replace(r'\([0-9]*\)','',regex=True)
            ah_pandas = ah_pandas[ah_pandas.stranka!='Unibet']
            ah_pandas = ah_pandas[ah_pandas.stranka!='bet365']
            for ah_set in ah_pandas.set.unique():
                for ah_gem in ah_pandas.gemy.unique():
                    for ah_jednotka_gemy in ah_pandas.loc[(ah_pandas.set==ah_set)&(ah_pandas.gemy==ah_gem)].iterrows():
                        for ah_dvojka_gemy in ah_pandas.loc[(ah_pandas.set==ah_set)&(ah_pandas.gemy==ah_gem)].iterrows():        
                            #print(f'set {ou_set} gem {gem} over {over[1].over} under {under[1].under}')
                            # ah_pandas[f'AH - {ah_set} | HANDICAP : {ah_gem} | JEDNOTKA : {ah_jednotka_gemy[1].stranka} - {ah_jednotka_gemy[1].jednotka_gemy} | DVOJKA : {ah_dvojka_gemy[1].stranka} - {ah_dvojka_gemy[1].dvojka_gemy}'] = pow(ah_jednotka_gemy[1].jednotka_gemy,-1) + pow(ah_dvojka_gemy[1].dvojka_gemy,-1)
                            ah_pandas[f'AH - {ah_set} | HANDICAP : {ah_gem} | JEDNOTKA : {ah_jednotka_gemy[1].stranka} - {ah_jednotka_gemy[1].jednotka_gemy} | DVOJKA : {ah_dvojka_gemy[1].stranka} - {ah_dvojka_gemy[1].dvojka_gemy}'] = ((100 / (ah_jednotka_gemy[1].jednotka_gemy/ah_dvojka_gemy[1].dvojka_gemy + 1))*ah_jednotka_gemy[1].jednotka_gemy)-100
            ah_pandas_results_first_col = ah_pandas.transpose().columns[0]
            ah_pandas_results = ah_pandas.transpose()[ah_pandas_results_first_col].drop(['set','stranka','gemy','jednotka_gemy','dvojka_gemy'])
            max_ah_pandas = ah_pandas_results.sort_values(ascending=False).head(1)

        except Exception as e:
            max_ah_pandas=pd.DataFrame([0])[0]
            #print(max_ah_pandas)
            print(f'Daco zle v AH. Skip. ID : {zapasy_id}, {e}')
            pass

        try:
            onextwo_pandas.loc[onextwo_pandas.jednotka=='-',"jednotka"]=1.00
            onextwo_pandas.loc[onextwo_pandas.x=='-',"x"]=1.00
            onextwo_pandas.loc[onextwo_pandas.dvojka=='-',"dvojka"]=1.00
            onextwo_pandas[onextwo_pandas.columns.difference(['set', 'stranka'])] = onextwo_pandas[onextwo_pandas.columns.difference(['set', 'stranka'])].astype(float)
            onextwo_pandas.set = onextwo_pandas.set.str.replace(r'\([0-9]*\)','',regex=True)
            onextwo_pandas = onextwo_pandas[onextwo_pandas.stranka!='Unibet']
            onextwo_pandas = onextwo_pandas[onextwo_pandas.stranka!='bet365']
            for onextwo_set in onextwo_pandas.set.unique():
                for onextwo_jednotka in onextwo_pandas.loc[onextwo_pandas.set==onextwo_set].iterrows():
                    for onextwo_dvojka in onextwo_pandas.loc[onextwo_pandas.set==onextwo_set].iterrows():
                        for onextwo_x in onextwo_pandas.loc[onextwo_pandas.set==onextwo_set].iterrows():
                            onextwo_pandas[f'1X2 - {onextwo_set} | JEDNOTKA : {onextwo_jednotka[1].stranka} - {onextwo_jednotka[1].jednotka} | X : {onextwo_x[1].stranka} - {onextwo_x[1].x} | DVOJKA : {onextwo_dvojka[1].stranka} - {onextwo_dvojka[1].dvojka}'] = ((100 / (1 + onextwo_jednotka[1].jednotka/onextwo_x[1].x + onextwo_jednotka[1].jednotka/onextwo_dvojka[1].dvojka ))*onextwo_jednotka[1].jednotka)-100
            onextwo_results_first_col = onextwo_pandas.transpose().columns[0]
            onextwo_results = onextwo_pandas.transpose()[onextwo_results_first_col].drop(['set','stranka','jednotka','dvojka','x'])
            max_onetwo_pandas = onextwo_results.sort_values(ascending=False).head(1)

        except Exception as e:
            max_onetwo_pandas=pd.DataFrame([0])[0]
            #print(max_ah_pandas)
            print(f'Daco zle v 1X2. Skip. ID : {zapasy_id}, {e}')
            pass

        try:
            ds_pandas.loc[ds_pandas.jednotkax=='-',"jednotkax"]=1.00
            ds_pandas.loc[ds_pandas.jednadva=='-',"jednadva"]=1.00
            ds_pandas.loc[ds_pandas.xdva=='-',"xdva"]=1.00
            ds_pandas[ds_pandas.columns.difference(['set', 'stranka'])] = ds_pandas[ds_pandas.columns.difference(['set', 'stranka'])].astype(float)
            ds_pandas.set = ds_pandas.set.str.replace(r'\([0-9]*\)','',regex=True)
            ds_pandas = ds_pandas[ds_pandas.stranka!='Unibet']
            ds_pandas = ds_pandas[ds_pandas.stranka!='bet365']

            max_values_from_onextwo_jednotka = onextwo_pandas.groupby('set').apply(lambda row: max_from_onextwo(row,'jednotka')).reset_index().drop(columns=['level_1'])
            max_values_from_onextwo_x = onextwo_pandas.groupby('set').apply(lambda row: max_from_onextwo(row,'x')).reset_index().drop(columns=['level_1'])
            max_values_from_onextwo_dvojka = onextwo_pandas.groupby('set').apply(lambda row: max_from_onextwo(row,'')).reset_index().drop(columns=['level_1'])



            for ds_set in ds_pandas.set.unique():
                max_jednotka_onextwo = max_values_from_onextwo_jednotka[max_values_from_onextwo_jednotka.set==ds_set]
                max_x_onextwo = max_values_from_onextwo_x[max_values_from_onextwo_x.set==ds_set]
                max_dvojka_onextwo = max_values_from_onextwo_dvojka[max_values_from_onextwo_dvojka.set==ds_set]
                for ds_jednotkax in ds_pandas.loc[ds_pandas.set==ds_set].iterrows():
                    for ds_jednadva in ds_pandas.loc[ds_pandas.set==ds_set].iterrows():
                        for ds_xdva in ds_pandas.loc[ds_pandas.set==ds_set].iterrows():
                            # ds_pandas[f'DŠ - {ds_set} | JEDNOTKAX : {ds_jednotkax[1].stranka} - {ds_jednotkax[1].jednotkax} | 1X2 DVOJKA : {max_dvojka_onextwo.stranka.values[0]} - {max_dvojka_onextwo.dvojka.values[0]}'] = pow(float(ds_jednotkax[1].jednotkax),-1) + pow(float(max_dvojka_onextwo.dvojka.values[0]),-1)
                            # ds_pandas[f'DŠ - {ds_set} | JEDNADVA : {ds_jednadva[1].stranka} - {ds_jednadva[1].jednadva} | 1X2 X : {max_x_onextwo.stranka.values[0]} - {max_x_onextwo.x.values[0]}'] = pow(float(ds_jednadva[1].jednadva),-1) + pow(float(max_x_onextwo.x.values[0]),-1)
                            # ds_pandas[f'DŠ - {ds_set} | XDVA : {ds_xdva[1].stranka} - {ds_xdva[1].xdva} | 1X2 JEDNOTKA : {max_jednotka_onextwo.stranka.values[0]} - {max_jednotka_onextwo.jednotka.values[0]}'] = pow(float(ds_xdva[1].xdva),-1) + pow(float(max_jednotka_onextwo.jednotka.values[0]),-1)
                            ds_pandas[f'DŠ - {ds_set} | JEDNOTKAX : {ds_jednotkax[1].stranka} - {ds_jednotkax[1].jednotkax} | 1X2 DVOJKA : {max_dvojka_onextwo.stranka.values[0]} - {max_dvojka_onextwo.dvojka.values[0]}'] = ((100 / (ds_jednotkax[1].jednotkax/max_dvojka_onextwo.dvojka.values[0] + 1))*ds_jednotkax[1].jednotkax)-100
                            ds_pandas[f'DŠ - {ds_set} | JEDNADVA : {ds_jednadva[1].stranka} - {ds_jednadva[1].jednadva} | 1X2 X : {max_x_onextwo.stranka.values[0]} - {max_x_onextwo.x.values[0]}'] = ((100 / (ds_jednadva[1].jednadva/max_x_onextwo.x.values[0] + 1))*ds_jednadva[1].jednadva)-100
                            ds_pandas[f'DŠ - {ds_set} | XDVA : {ds_xdva[1].stranka} - {ds_xdva[1].xdva} | 1X2 JEDNOTKA : {max_jednotka_onextwo.stranka.values[0]} - {max_jednotka_onextwo.jednotka.values[0]}'] = ((100 / (ds_xdva[1].xdva/max_jednotka_onextwo.jednotka.values[0] + 1))*ds_xdva[1].xdva)-100
            ds_results_first_col = ds_pandas.transpose().columns[0]
            ds_results = ds_pandas.transpose()[ds_results_first_col].drop(['set','stranka','jednotkax','jednadva','xdva'])
            max_ds_pandas = ds_results.sort_values(ascending=False).head(1)

        except Exception as e:
            max_ds_pandas=pd.DataFrame([0])[0]
            #print(max_home_away)
            print(f'Daco zle v DŠ. Skip. ID : {zapasy_id} , {e}')
            pass
        ##################################################################################################

        check_for_msg = max_home_away.append([max_ou_pandas,max_ah_pandas,max_onetwo_pandas,max_ds_pandas]).sort_values(ascending=False).head(1)
        print(check_for_msg, zapasy_id)
        if(check_for_msg.values[0]>=2.5):
            df_check = pd.read_csv(r'checked.csv')
            record_for_msg_rounded = float("%.2f" % check_for_msg.values[0])
            if(df_check[df_check.match==zapasy_id].empty):
                empty = True
            else:
                empty = False
            if(empty==False):
                if(df_check[df_check.match==zapasy_id].sort_values(by='value',ascending=False).head(1).value.values[0]<record_for_msg_rounded):
                    empty=True
            if(empty==True):
                # record_for_msg_rounded = float("%.2f" % check_for_msg.values[0])
                check_for_msg_enter = check_for_msg.index[0].replace(r'|','\n')
                message = f'{check_for_msg_enter} \n PROFIT - {record_for_msg_rounded} % \n Match : {zapasy_id}'
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(url))
                df_check = df_check.append({'match':zapasy_id,'value':record_for_msg_rounded},ignore_index=True)
                df_check.to_csv(r'checked.csv',index=False)
    except Exception as e:
        pass
    #driver_zapas.quit()
        

if __name__ == '__main__':
    day = int(sys.argv[1])
    while(True):
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(endpoint)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME,"calendar__navigation--tomorrow")))

            if(day==1):
                driver.execute_script("arguments[0].click();", driver.find_element_by_class_name("calendar__navigation--tomorrow"))
            if(day==2):
                driver.execute_script("arguments[0].click();", driver.find_element_by_class_name("calendar__navigation--tomorrow"))
                time.sleep(5)
                driver.execute_script("arguments[0].click();", driver.find_element_by_class_name("calendar__navigation--tomorrow"))
        
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//*[@id='live-table']/div[1]/div[1]/div[5]")))
            driver.execute_script("arguments[0].click();", driver.find_element_by_xpath("//*[@id='live-table']/div[1]/div[1]/div[5]"))

            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH,"//div[@title='Klikni pre detail zápasu!']")))
            rozkliknut = driver.find_elements_by_xpath("//div[@title='Zobraziť všetky zápasy tejto ligy!']")

            for x in rozkliknut:
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(x))
                    driver.execute_script("arguments[0].click();", x)
                except Exception as e:
                    # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(x))
                    # driver.execute_script("arguments[0].click();", x)
                    print(e)
            zapasy = driver.find_elements_by_xpath("//div[@title='Klikni pre detail zápasu!']")
            zapasy_id = []
            regexes = [
                "Koniec.*",
                "Postup bez boja.*",
                "Zrušené.*",
                "[0-9]. set.*",
                "[0-9]. štvrtina.*",
                "Live.*",
                "Prestávka.*",
                "Čakáme aktualizáciu.*",
                "Odložené.*",
                "Po predĺžení.*",
                "Predĺženie.*"
            ]
            combined = "(" + ")|(".join(regexes) + ")"
            [zapasy_id.append(x.get_attribute('id')[4:]) for x in zapasy if not re.match(combined,x.find_element_by_xpath(f"//*[@id='{x.get_attribute('id')}']/div[2]").text)]
            urls_full = []
            for x in zapasy_id:
                urls_full.append(f'https://www.flashscore.sk/zapas/{x}/#/porovnanie-kurzov/')
            driver.quit()
            threadLocal = threading.local()
            urls_len = len(urls_full)
            number_of_processes = min(4, urls_len)
            print(f'ZACINAM CHECK {urls_len} in {day}.')
            with ThreadPool(processes=number_of_processes) as pool:
                result_array = pool.map(check_multithread, urls_full)

                # Must ensure drivers are quitted before threads are destroyed:
                del threadLocal
                # This should ensure that the __del__ method is run on class Driver:
                gc.collect()

                pool.close()
                pool.join()
            print(f'DONE {urls_len} in {day}.')
        except Exception as e:
            driver.quit()
            print(f'Error in {day} : {e}')
            pass
        