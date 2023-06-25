sport = 'FUTBAL'

def golvobochpolcasoch(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n ÁNO : {jednotka[1].stranka} : {jednotka[1].áno} \n NIE : {dvojka[1].stranka} : {dvojka[1].nie}'] = ((100 / (jednotka[1].áno/dvojka[1].nie + 1))*jednotka[1].áno)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'gol v oboch polcasoch exception {e}')
        return None


def obidvapolcasy(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n ÁNO : {jednotka[1].stranka} : {jednotka[1].áno} \n NIE : {dvojka[1].stranka} : {dvojka[1].nie}'] = ((100 / (jednotka[1].áno/dvojka[1].nie + 1))*jednotka[1].áno)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'obidvapolcasy exception {e}')
        return None

def asponjedenpolcas(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n ÁNO : {jednotka[1].stranka} : {jednotka[1].áno} \n NIE : {dvojka[1].stranka} : {dvojka[1].nie}'] = ((100 / (jednotka[1].áno/dvojka[1].nie + 1))*jednotka[1].áno)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'aspon jeden polcas exception {e}')
        return None

def pocetfaulov(dff,cat):
    try:
        results = {}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        columns = []
        for column in dff.columns:
            if(column!='stranka'):
                column_to_insert = column.split('ako ')
                columns.append(column_to_insert[1])
        columns = list(dict.fromkeys(columns))
        for column in columns:
            menej = f'menej ako {column}'
            viac = f'viac ako {column}'
            for jednotka in dff.iterrows():
                for dvojka in dff.iterrows():
                    try:
                        results[f'{cat} \n {menej} : {jednotka[1].stranka} : {jednotka[1][menej]} \n {viac} : {dvojka[1].stranka} : {dvojka[1][viac]}'] = ((100 / (jednotka[1][menej]/dvojka[1][viac] + 1))*jednotka[1][menej])-100
                    except:
                        continue
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'pocetfaulov exception {e}')
        return None

def strelynabranu(dff,cat):
    try:
        results = {}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        columns = []
        for column in dff.columns:
            if(column!='stranka'):
                column_to_insert = column.split('ako ')
                columns.append(column_to_insert[1])
        columns = list(dict.fromkeys(columns))
        for column in columns:
            menej = f'menej ako {column}'
            viac = f'viac ako {column}'
            for jednotka in dff.iterrows():
                for dvojka in dff.iterrows():
                    try:
                        results[f'{cat} \n {menej} : {jednotka[1].stranka} : {jednotka[1][menej]} \n {viac} : {dvojka[1].stranka} : {dvojka[1][viac]}'] = ((100 / (jednotka[1][menej]/dvojka[1][viac] + 1))*jednotka[1][menej])-100
                    except:
                        continue
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'strelynabranu exception {e}')
        return None

def penaltavzapase(dff,cat):
    try:
        dff = dff.rename(columns = {'menej ako 0.5':'nie','viac ako 0.5':'áno'})
        dff = dff.groupby(level=0, axis=1).apply(lambda x: x.apply(same_merge, axis=1))
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n ÁNO : {jednotka[1].stranka} : {jednotka[1].áno} \n NIE : {dvojka[1].stranka} : {dvojka[1].nie}'] = ((100 / (jednotka[1].áno/dvojka[1].nie + 1))*jednotka[1].áno)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'penalta v zapase exception {e}')
        return None

def pocetrohov(dff,cat):
    try:
        results = {}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        columns = []
        for column in dff.columns:
            if(column!='stranka'):
                column_to_insert = column.split('ako ')
                columns.append(column_to_insert[1])
        columns = list(dict.fromkeys(columns))
        for column in columns:
            menej = f'menej ako {column}'
            viac = f'viac ako {column}'
            for jednotka in dff.iterrows():
                for dvojka in dff.iterrows():
                    try:
                        results[f'{cat} \n {menej} : {jednotka[1].stranka} : {jednotka[1][menej]} \n {viac} : {dvojka[1].stranka} : {dvojka[1][viac]}'] = ((100 / (jednotka[1][menej]/dvojka[1][viac] + 1))*jednotka[1][menej])-100
                    except:
                        continue
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'pocetrohov exception {e}')
        return None

def viacrohov(dff,cat):
    try:
        results ={}
        dff = dff.rename(columns={'remíza':'rovnako'})
        dff = dff.groupby(level=0, axis=1).apply(lambda x: x.apply(same_merge, axis=1))
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                for xko in dff.iterrows():
                    results[f'{cat} \n JEDNOTKA : {jednotka[1].stranka} : {jednotka[1].jednotka} \n ROVNAKO : {xko[1].stranka} : {xko[1].rovnako} \n DVOJKA : {dvojka[1].stranka} : {dvojka[1].dvojka}'] = ((100 / (1 + jednotka[1].jednotka/xko[1].rovnako + jednotka[1].jednotka/dvojka[1].dvojka ))*jednotka[1].jednotka)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'viacrohov exception {e}')
        return None

def prvyroh(dff,cat):
    try:
        results ={}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                for xko in dff.iterrows():
                    results[f'{cat} \n JEDNOTKA : {jednotka[1].stranka} : {jednotka[1].jednotka} \n NIKTO : {xko[1].stranka} : {xko[1].nikto} \n DVOJKA : {dvojka[1].stranka} : {dvojka[1].dvojka}'] = ((100 / (1 + jednotka[1].jednotka/xko[1].nikto + jednotka[1].jednotka/dvojka[1].dvojka ))*jednotka[1].jednotka)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'prvyroh exception {e}')
        return None

def same_merge(x): return ','.join(x[x.notnull()].astype(str))

def polcassviacgolmi(dff,cat):
    try:
        results ={}
        dff = dff.rename(columns={'v 1. polčase':'prvy_polčas','v 2. polčase':'druhy_polčas','v oboch rovnako':'rovnako','1. polčas':'prvy_polčas','2. polčas':'druhy_polčas'})
        dff = dff.groupby(level=0, axis=1).apply(lambda x: x.apply(same_merge, axis=1))
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                for xko in dff.iterrows():
                    results[f'{cat} \n PRVY POLČAS : {jednotka[1].stranka} : {jednotka[1].prvy_polčas} \n ROVNAKO : {xko[1].stranka} : {xko[1].rovnako} \n DRUHY POLČAS : {dvojka[1].stranka} : {dvojka[1].druhy_polčas}'] = ((100 / (1 + jednotka[1].prvy_polčas/xko[1].rovnako + jednotka[1].prvy_polčas/dvojka[1].druhy_polčas ))*jednotka[1].prvy_polčas)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'polcas s viac golmi exception {e}')
        return None

def obajadajugol(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n ÁNO : {jednotka[1].stranka} : {jednotka[1].áno} \n NIE : {dvojka[1].stranka} : {dvojka[1].nie}'] = ((100 / (jednotka[1].áno/dvojka[1].nie + 1))*jednotka[1].áno)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'obaja daju gol exception {e}')
        return None

def prvygol(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        #print(dff)
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                for xko in dff.iterrows():
                    results[f'{cat} \n JEDNOTKA : {jednotka[1].stranka} : {jednotka[1].jednotka} \n NIKTO : {xko[1].stranka} : {xko[1].nikto} \n DVOJKA : {dvojka[1].stranka} : {dvojka[1].dvojka}'] = ((100 / (1 + jednotka[1].jednotka/xko[1].nikto + jednotka[1].jednotka/dvojka[1].dvojka ))*jednotka[1].jednotka)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'prvygol exception {e}')
        return None



def AH(dff,cat):
    try:
        results = {}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        columns = []
        for column in dff.columns:
            if(column!='stranka'):
                column_to_insert = column.split(' ')
                columns.append(column_to_insert[1])
        columns = list(dict.fromkeys(columns))
        for column in columns:
            jednotka_znamienko = '-'
            dvojka_znamienko = '+'
            if('-' in column):
                cislo = column.split('-')
            else:
                jednotka_znamienko = '+'
                dvojka_znamienko = '-'
                cislo = column.split('+')
            menej = f'jednotka {jednotka_znamienko}{cislo[1]}'
            viac = f'dvojka {dvojka_znamienko}{cislo[1]}'
            for jednotka in dff.iterrows():
                for dvojka in dff.iterrows():
                    try:
                        results[f'{cat} \n {menej} : {jednotka[1].stranka} : {jednotka[1][menej]} \n {viac} : {dvojka[1].stranka} : {dvojka[1][viac]}'] = ((100 / (jednotka[1][menej]/dvojka[1][viac] + 1))*jednotka[1][menej])-100
                    except:
                        continue
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'AH exception {e}')
        return None

def HA(dff,cat):
    try:
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        results ={}
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                 results[f'{cat} \n JEDNOTKA : {jednotka[1].stranka} : {jednotka[1].jednotka} \n DVOJKA : {dvojka[1].stranka} : {dvojka[1].dvojka}'] = ((100 / (jednotka[1].jednotka/dvojka[1].dvojka + 1))*jednotka[1].jednotka)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'HA exception {e}')
        return None

def other(dff,cat):
    results = {}
    return results

def OU(dff,cat):
    try:
        results = {}
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        columns = []
        for column in dff.columns:
            if(column!='stranka'):
                column_to_insert = column.split('ako ')
                columns.append(column_to_insert[1])
        columns = list(dict.fromkeys(columns))
        for column in columns:
            menej = f'menej ako {column}'
            viac = f'viac ako {column}'
            for jednotka in dff.iterrows():
                for dvojka in dff.iterrows():
                    try:
                        results[f'{cat} \n {menej} : {jednotka[1].stranka} : {jednotka[1][menej]} \n {viac} : {dvojka[1].stranka} : {dvojka[1][viac]}'] = ((100 / (jednotka[1][menej]/dvojka[1][viac] + 1))*jednotka[1][menej])-100
                    except:
                        continue
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'OU exception {e}')
        return None


def send(max_df,match,time,match_nike):
    TOKEN = "5717884327:AAG1XYqDvCJMB1cpE3PlnjipwZv2rzOS8ns"
    chat_id = "-1001695455818"
    message="test"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    try:
        max_df = max_df.reset_index()
        max_df_dict = max_df.to_dict()
        key = max_df_dict['index'][0]
        value = max_df_dict[0][0]
        if(value>1):
            df_check = pd.read_csv(r'checked_new.csv')
            if(df_check[df_check.match==match].empty):
                empty = True
            else:
                empty = False
            if(empty==False):
                if(df_check[df_check.match==match].sort_values(by='value',ascending=False).head(1).value.values[0]<value):
                    empty=True
            if(empty==True):
                record_for_msg_rounded = float("%.2f" % value)
                key = key.replace('Zápas','')
                key = key.replace('Both','')
                message = f'------------------------------ \n SPORT - {sport} \n {key} \n PROFIT : {record_for_msg_rounded} % \n MATCH_TIPSPORT : {match} \n MATCH_NIKE : {match_nike} \n TIME : {time} '
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                print(requests.get(url))
                try:
                    url_lambda = 'https://cdyvrd8716.execute-api.eu-central-1.amazonaws.com/dev/new'
                    content_lambda={}
                    content_lambda['body']=message
                    requests.post(url_lambda,data=json.dumps(content_lambda),timeout=2)
                except Exception as e:
                    pass
                df_check = df_check.append({'match':match,'value':value},ignore_index=True)
                df_check.to_csv(r'checked_new.csv',index=False)
        return f'{key} {value}'
    except Exception as e:
        print(f'send {e}')
        return None

from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

def find_most_similiar(nike_match,tipsport_matches):
    result = ''
    highest = 0
    for tipsport in tipsport_matches:
        povodny_tipsport = tipsport
        #tipsport = tipsport.lower()
        #nike_match = nike_match.lower()
        tipsport = tipsport.replace(' - ',' ')
        nike_match = nike_match.replace('-',' ')
        res = similar(nike_match,tipsport) * 100
        if res>highest:
            highest=res
            result=povodny_tipsport

    #print(highest)
    if highest<60:
        return None
    return result

class Driver:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def __del__(self):
        try:
            self.driver.quit() # clean up driver when we are cleaned up
            print('The driver has been "quitted".')
        except:
            print('Error in deleting driver. Pass')
            pass
            
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
    
    
    
def calculate1X2DS(dff,cat):
    try:
        dff = dff.rename(columns={'1x':'_1X','12':'_12','x2':'_X2'})
        dff[dff.columns.difference(['stranka'])] = dff[dff.columns.difference(['stranka'])].astype(float)
        max_jednotka = dff[dff.jednotka==dff.jednotka.max()][['stranka','jednotka']]
        max_xko = dff[dff.remíza==dff.remíza.max()][['stranka','remíza']]
        max_dvojka = dff[dff.dvojka==dff.dvojka.max()][['stranka','dvojka']]
        results = {}
        for jednotka in dff.iterrows():
            for dvojka in dff.iterrows():
                for xko in dff.iterrows():
                    results[f'{cat} \n JEDNOTKA : {jednotka[1].stranka} : {jednotka[1].jednotka} \n X : {xko[1].stranka} : {xko[1].remíza} \n DVOJKA : {dvojka[1].stranka} : {dvojka[1].dvojka}'] = ((100 / (1 + jednotka[1].jednotka/xko[1].remíza + jednotka[1].jednotka/dvojka[1].dvojka ))*jednotka[1].jednotka)-100

        for jednotkax in dff.iterrows():
            for xdvojka in dff.iterrows():
                for jednadva in dff.iterrows():
                    results[f'{cat} \n JEDNOTKAX : {jednotkax[1].stranka} : {jednotkax[1]._1X} \n DVOJKA : {max_dvojka.stranka.values[0]} : {max_dvojka.dvojka.values[0]}'] = ((100 / (jednotkax[1]._1X/max_dvojka.dvojka.values[0] + 1))*jednotkax[1]._1X)-100
                    results[f'{cat} \n JEDNADVA : {jednadva[1].stranka} : {jednadva[1]._12} \n X : {max_xko.stranka.values[0]} : {max_xko.remíza.values[0]}'] = ((100 / (jednadva[1]._12/max_xko.remíza.values[0] + 1))*jednadva[1]._12)-100
                    results[f'{cat} \n XDVA : {xdvojka[1].stranka} : {xdvojka[1]._X2} \n JEDNOTKA : {max_jednotka.stranka.values[0]} : {max_jednotka.jednotka.values[0]}'] = ((100 / (xdvojka[1]._X2/max_jednotka.jednotka.values[0] + 1))*xdvojka[1]._X2)-100
        key_max = max(results, key=results.get)
        value_max = results[max(results, key=results.get)]
        max_res = {key_max:value_max}
        print(max_res)
        return max_res
    except Exception as e:
        print(f'calculate1X2DS {e}')
        return None
    
def calculateArbitrageAndSend(df,match,time,match_nike):
    try:
        all_df = pd.DataFrame()
        df = df[df.full!='Každý tím dá v zápase 2 a viac gólov']
        df = df[df.full!='Každý tím dá v zápase 2 a viac gólov']
        for category in df.category.unique():
            for polcas in df[df.category==category].time.unique():
                for team in df[(df.category==category)&(df.time==polcas)].team.unique():
                    dff = pd.DataFrame()
                    for stranka in df[(df.category==category)&(df.time==polcas)&(df.team==team)].iterrows():
                        dinsert = {}
                        dinsert['stranka']=stranka[1].stranka
                        try:
                            for key, value in stranka[1].bets.items():
                                key_lower = key.lower()
                                dinsert[key_lower]=value
                            dff=dff.append(dinsert,ignore_index=True)
                        except:
                            continue
                    cat = f'{category} {polcas} {team}'
                    if(category=='1X2'):
                        results = calculate1X2DS(dff,cat)
                    elif(category=='Počet gólov'):
                        results = OU(dff,cat)
                    elif(category=='Víťaz zápasu bez remízy'):
                        results = HA(dff,cat)
                    elif(category=='Handicap'):
                        results = AH(dff,cat)
                    elif(category=='1. gól'):
                        results = prvygol(dff,cat)
                    elif(category=='Každý tím dá 1 a viac gólov'):
                        results = obajadajugol(dff,cat)
                    elif(category=='V ktorom polčase padne najviac gólov'):
                        results = polcassviacgolmi(dff,cat)
                    elif(category=='Kto bude kopať v zápase 1. roh'):
                        results = prvyroh(dff,cat)
                    elif(category=='Viac rohov v zápase'):
                        results = viacrohov(dff,cat)
                    elif(category=='Počet rohov'):
                        results = pocetrohov(dff,cat)
                    elif(category=='Penalta v zápase'):
                        results = penaltavzapase(dff,cat)
                    elif(category=='Počet striel na bránu'):
                        results = strelynabranu(dff,cat)
                    elif(category=='Počet faulov'):
                        results = pocetfaulov(dff,cat)
                    elif(category=='Tím vyhrá aspoň jeden polčas'):
                        results = asponjedenpolcas(dff,cat)
                    elif(category=='Tím vyhrá obidva polčasy'):
                        results = obidvapolcasy(dff,cat)
                    elif(category=='Tím dá gól v oboch polčasoch'):
                        results = golvobochpolcasoch(dff,cat)
                    else:
                        results=other(dff,cat)
                    all_df = all_df.append(results,ignore_index=True)
        all_df = all_df.max().reset_index()
        all_df_max = all_df[all_df[0]==all_df[0].max()]
        return send(all_df_max,match,time,match_nike)
    except Exception as e:
        print(f'calculatearbitrageandsend {e}')
        return None
    
    
def check_multithread(matches):
    print(f'start {matches}')
    if(matches == 'Celkové umiestnenie'):
        return None
    try:

        driver_fortuna = Driver.create_driver()
        driver_fortuna.get(endpoint_fortuna)
        try:
            WebDriverWait(driver_fortuna, 20).until(EC.element_to_be_clickable(driver_fortuna.find_element_by_id('cookie-consent-button-accept')))
            driver_fortuna.execute_script("arguments[0].click();",driver_fortuna.find_element_by_id('cookie-consent-button-accept'))
            WebDriverWait(driver_fortuna, 20).until(EC.element_to_be_clickable(driver_fortuna.find_element_by_class_name('live-disabled-filter-label')))
            driver_fortuna.execute_script("arguments[0].click();",driver_fortuna.find_element_by_class_name('live-disabled-filter-label'))
            WebDriverWait(driver_fortuna, 20).until(EC.element_to_be_clickable(driver_fortuna.find_element_by_class_name('events-list')))
        except:
            pass

        reached_page_end = False
        last_height = driver_fortuna.execute_script("return document.body.scrollHeight")

        while not reached_page_end:
            driver_fortuna.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = driver_fortuna.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                    reached_page_end = True
            else:
                    last_height = new_height
        driver_fortuna.execute_script("window.scrollTo(0, 0);")

        events_list_fortuna_raw = driver_fortuna.find_elements_by_xpath('//tr')
        events_list_filtered_fortuna = []
        matches_thread_fortuna_text = []
        for raw in events_list_fortuna_raw:
            if(raw.text == '' or 'Výsledok' in raw.text):
                continue
            title_fortuna = raw.find_element_by_class_name('col-title')
            title_fortuna = title_fortuna.find_element_by_class_name('market-name').text
            title_fortuna = title_fortuna.replace('BetBuilder','')
            title_fortuna = title_fortuna.replace('\n','')
            matches_thread_fortuna_text.append(title_fortuna)


        driver_tipsport = Driver.create_driver()
        #driver_tipsport = webdriver.Chrome(options=chrome_options,service=s)
        driver_tipsport.get(endpoint_tipsport)
        WebDriverWait(driver_tipsport, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"o-matchRow")))
        rows_tipsport = driver_tipsport.find_elements_by_class_name("o-matchRow")

        matches_thread_tipsport_text = []

        for row in rows_tipsport:
            match_name = row.find_element_by_class_name('o-matchRow__matchName')
            matches_thread_tipsport_text.append(match_name.text)

        driver = Driver.create_driver()
        #driver = webdriver.Chrome(options=chrome_options,service=s)
        driver.get(endpoint)
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"boxes-inner-view")))
        wrapper = driver.find_element_by_class_name("boxes-inner-view")

        while True:
            try:
                WebDriverWait(driver, 60).until(EC.element_to_be_clickable(wrapper.find_element_by_class_name('btn-primary')))
                driver.execute_script("arguments[0].click();", wrapper.find_element_by_class_name('btn-primary'))
            except Exception as e:
                break 

        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"boxes-inner-view")))
        wrapper = driver.find_element_by_class_name("boxes-inner-view")
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"bg-dark-futbal")))
        leagues = wrapper.find_elements_by_class_name("bg-dark-futbal")

        row = ''
        break_c = False
        for i,league in enumerate(leagues):
            rows_inside_league = league.find_elements_by_class_name("bet-view-prematch-row")
            for y,rows in enumerate(rows_inside_league):
                try:
                    team = rows.find_element_by_class_name('bets-opponents').text.replace('\n','')
                    team = team.replace('vs',' - ')
                    if team==matches:
                        row = rows
                        break_c = True
                        break
                except:
                    continue
            if(break_c == True):
                break 

        df = pd.DataFrame()

        try:
            team = row.find_element_by_class_name('bets-opponents').text.replace('\n','')
            team = team.replace('vs',' - ')
            nazov_nike = row.find_element_by_class_name('bets-opponents').text.replace('\n','')
            nazov_nike = nazov_nike.replace('vs',' - ')
            if(team=='Celkové umiestnenie'):
                print('Celkové umiestnenie skip')
                return None
            paired = find_most_similiar(team,matches_thread_tipsport_text)
            # if(paired == None):
            #     print('Nie je pár tipsport')
            #     return None
            paired_fortuna = find_most_similiar(team,matches_thread_fortuna_text)
            if(paired == None and paired_fortuna == None):
                print('Nie je ani jeden par')
                return None

            print(f'{team} ---- {paired} ---- {paired_fortuna}')
            splitted = team.split(' - ')
            first_team = splitted[0]
            second_team = splitted[1]
            #print(f'{first_team} - {second_team}')
            more_bets = row.find_element_by_class_name('odd-bet-number')
            driver.execute_script("arguments[0].click();", more_bets)
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"se-detail-3")))
            WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"market-accordion-btn")))
            #time.sleep(10)
            all_bets_container = driver.find_element_by_class_name('se-detail-3')
            all_opps = all_bets_container.find_elements_by_class_name('market-accordion-btn')
            ##ALL OPPS (SUPERSANCA,ZAPAS ATD)
            #print(len(all_opps))
            #all_bets = all_bets_container.find_elements_by_class_name('bet-group-box-table')
            all_bets = all_bets_container.find_elements_by_css_selector("[aria-expanded='true']")
            indexes_to_delete = []
            #VSETKY KURZY
           #print(len(all_bets))
            for i,opp in enumerate(all_opps):
                text_to_check  = opp.text.replace(first_team,'jednotka')
                text_to_check = text_to_check.replace(second_team,'dvojka')
                if text_to_check not in potrebujem_nike:
                    indexes_to_delete.append(i)
            for i,opp in enumerate(all_opps):
                if i in indexes_to_delete:
                    continue
                dict_to_append = {}
                oppurtunity_team_replaced = opp.text.replace(first_team,'jednotka')
                oppurtunity_team_replaced = oppurtunity_team_replaced.replace(second_team,'dvojka')
              #  print(f'{oppurtunity_team_replaced}')
                polcas = 'Zápas'
                team = 'Both'
                if any(substring in oppurtunity_team_replaced for substring in first_halftime) == True:
                    polcas='1.polčas'
                elif any(substring in oppurtunity_team_replaced for substring in second_halftime) == True:
                    polcas='2.polčas'
                if 'jednotka' in oppurtunity_team_replaced:
                    team='jednotka'
                elif 'dvojka' in oppurtunity_team_replaced:
                    team='dvojka'
                #print(f'{polcas} {team}')
                try:
                    dict_to_append['category'] = slovnik_nike_futbal[oppurtunity_team_replaced]
                except:
                    dict_to_append['category'] = slovnik_nike_futbal['']
                   # print(f'neni {oppurtunity_team_replaced}')
                dict_to_append['time']=polcas
                dict_to_append['team']=team
                #print(dict_to_append)
                bets_dict = {}
                for row in all_bets[i].find_elements_by_class_name('bets-row'):
                    nazvy = row.find_elements_by_class_name('bet-left')
                    hodnoty = row.find_elements_by_class_name('bet-right')
                    for nazov,hodnota in zip(nazvy,hodnoty):
                        hodnota_to_check = hodnota.text
                        if(hodnota_to_check == ''):
                            hodnota_to_check=1.00
                        team1 = nazov.text.replace(first_team,'jednotka')
                        team1 = team1.replace(second_team,'dvojka')
                        #print(f'{team1} {hodnota_to_check}')
                        bets_dict[team1]=hodnota_to_check
                #if(dict_to_append['category']=='1X2'):
                dict_to_append['bets']=bets_dict
                dict_to_append['full']=oppurtunity_team_replaced
                #dict_to_append['match']=f'{first_team} - {second_team}'
                dict_to_append['stranka']='nike'
                df = df.append(dict_to_append,ignore_index=True)
            time_nike = driver.find_element_by_class_name('reakt-scoreboard-period').text
            match_name_tipsport = None
            match_name_fortuna = None
            if(paired != None):
                driver_tipsport = Driver.create_driver()
                driver_tipsport.get(endpoint_tipsport)
                WebDriverWait(driver_tipsport, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"o-matchRow")))
                rows_tipsport = driver_tipsport.find_elements_by_class_name("o-matchRow")
                tipsport_match = ''
                for rows_tipsport_for_match in rows_tipsport:
                    match_name = rows_tipsport_for_match.find_element_by_class_name('o-matchRow__matchName').text
                    if match_name==paired:
                        tipsport_match = rows_tipsport_for_match
                        break
                match_name_tipsport = tipsport_match.find_element_by_class_name('o-matchRow__matchName').text
                df = findTipsport(driver_tipsport,tipsport_match,df)
                res_to_print = df.to_dict('records')
            #print(f'{res_to_print} result')
            res = calculateArbitrageAndSend(df,match_name_tipsport,time_nike,nazov_nike)
            print(res)
            
        except Exception as e:
            print(f'Vseobecna chyba {matches} - {e}')
            return None
                  
                  
        return None
    except Exception as e:
        print(f'Didnt find any match with name {matches} {e}')
        return None              
    





def findTipsport(driver_tipsport,row,df):
    try:
        driver_tipsport.execute_script("arguments[0].click();", row)
        #time.sleep(10)
        WebDriverWait(driver_tipsport, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"o-matchRow__matchName")))
        match_name = row.find_element_by_class_name('o-matchRow__matchName')
        #print(match_name.text)
        splitted = match_name.text.split(' - ')
        first_team = splitted[0]
        second_team = splitted[1]
        # print(f'{first_team} - {second_team}')
        WebDriverWait(driver_tipsport, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"eventTable")))
        WebDriverWait(driver_tipsport, 60).until(EC.visibility_of_element_located((By.CLASS_NAME,"m-statsColumn__opportunityName")))
        skratene = driver_tipsport.find_elements_by_class_name('m-statsColumn__opportunityName')
        first_team = skratene[0].text
        second_team = skratene[2].text
        eventTables = driver_tipsport.find_elements_by_class_name('eventTable')
        for event in eventTables:
            dict_to_append = {}
            bet_name = event.find_element_by_class_name('eventTableHeaderWrapper')
            if(bet_name.text not in potrebujem_tipsport):
                continue
            bet_name = event.find_element_by_class_name('eventTableHeaderWrapper')
            table = event.find_element_by_class_name('tbodyEventTable')
            table_row = table.find_elements_by_class_name('trEventTable')
            #if(len(table_row)==0):
            table_columns = table.find_elements_by_class_name('columnTable')
        # print(bet_name.text)
            dict_to_append['full']=bet_name.text
            #dict_to_append['match']=match_name.text
            polcas = 'Zápas'
            if any(substring in bet_name.text for substring in first_halftime_tipsport) == True:
                polcas='1.polčas'
            elif any(substring in bet_name.text for substring in second_halftime_tipsport) == True:
                polcas='2.polčas'
            try:
                dict_to_append['category'] = slovnik_tipsport_futbal[bet_name.text]
            except:
                dict_to_append['category'] = slovnik_tipsport_futbal['']
            dict_to_append['time']=polcas
            dict_to_append['stranka']='tipsport'
            bets_dict = {}
            team_at_end = None
            if(len(table_columns)!=0):
                dict_to_append['team']='Both'
                llist =  []
                for table_column in table_columns:
                    team_col = table_column.find_elements_by_class_name('tdEventTable')
                    lllist = []
                    for tcol in team_col:
                        lllist.append(tcol.text)
                    llist.append(lllist)
                #print(llist)
                try:
                    transposed_list = np.transpose(llist)
                    tlist_to_list = transposed_list.tolist()
                    for tlist in tlist_to_list:
                        for tinnertlist in tlist:
                            vals = tinnertlist.split('\n')
                            bet = vals[0].replace(first_team,'jednotka')
                            bet = bet.replace(second_team,'dvojka')
                            value = float(vals[1])
                            bets_dict[bet]=value
                    dict_to_append['bets']=bets_dict
                except Exception as e:
                    pass
                
            for table_r in table_row:
                try:
                    team = table_r.find_element_by_class_name('tdEventName').text
                    team = team.replace(first_team,'jednotka')
                    team = team.replace(second_team,'dvojka')
                except:
                    team = 'Both'
                if(team_at_end != None and team_at_end!=team):
                    df = df.append(dict_to_append,ignore_index=True)
                    dict_to_append['bets']=''
                    bets_dict = {}
                    #dict_list.append(dict_to_append)
                if(team not in ['jednotka','dvojka','Both']):
                    #print(team)
                    dict_to_append['full'] = bet_name.text + f' {team}'
                    team='Both'
                oppurtunity = table_r.find_elements_by_class_name('opportunity')
                for opp in oppurtunity:
                    bet = opp.find_element_by_class_name('name').text
                    bet = bet.replace(first_team,'jednotka')
                    bet = bet.replace(second_team,'dvojka')
                    bet = bet.replace('Neprehra jednotka','1X')
                    bet = bet.replace('Nebude remíza','12')
                    bet = bet.replace('Neprehra dvojka','X2')
                    try:
                        value = opp.find_element_by_class_name('value').text
                    except:
                        value = '1.0'
                    # if(bet in bets_dict.keys()):
                    #     df = df.append(dict_to_append,ignore_index=True)
                    #     bets_dict = {}
                    bets_dict[bet]=value
                    #print(f'{polcas} - {team} - {bet} - {value}')
                    dict_to_append['bets']=bets_dict
                dict_to_append['team']=team
                team_at_end = team
            #if(dict_to_append['category']=='1X2'):
            team_at_end = None
            df = df.append(dict_to_append,ignore_index=True)
                    #print(dict_to_append)
        driver_tipsport.execute_script("arguments[0].click();", row)
    except Exception as e:
        print(f'FindTipsport error {e}')
        pass
    return df
    
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
from difflib import SequenceMatcher
import numpy as np
from time import sleep
import random
import json
import copy
import warnings
import sys
import time
import datetime
warnings.filterwarnings("ignore")

today = datetime.datetime.today().strftime('%Y-%m-%d')
tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
tomorrow = tomorrow.strftime('%Y-%m-%d')

endpoint_fortuna = f'https://www.ifortuna.sk/stavkovanie/futbal?selectDates=1&date={today}'
endpoint_fortuna_tomorrow = f'https://www.ifortuna.sk/stavkovanie/futbal?selectDates=1&date={tomorrow}'

endpoint = 'https://www.nike.sk/tipovanie/futbal?dnes'
endpoint_zajtra = 'https://www.nike.sk/tipovanie/futbal?zajtra'

endpoint_tipsport = 'https://www.tipsport.sk/kurzy/futbal-16?timeFilter=form.period.today&limit=1000'
endpoint_tipsport_zajtra = 'https://www.tipsport.sk/kurzy/futbal-16?timeFilter=form.period.tomorrow&limit=1000'

first_halftime_tipsport = ['1.polčas','1. polčas','1.pol','1. pol','1. polčasu','1.polčasu','1. polčase','1.polčase']
second_halftime_tipsport = ['2.polčas','2. polčas','2.pol','2. pol', '2. polčasu','2.polčasu','2. polčase','2.polčasu']

first_halftime_fortuna = ['1.polčas','1. polčas','1.pol','1. pol','1. polčasu','1.polčasu','1. polčase','1.polčase','1.poločas','1. poločas']
second_halftime_fortuna = ['2.polčas','2. polčas','2.pol','2. pol', '2. polčasu','2.polčasu','2. polčase','2.polčasu','2.poločas','2. poločas']

slovnik_tipsport_futbal = {'':'not found',
                        'Výsledok zápasu':'1X2',
                       'Výsledok 1. polčasu':'1X2',
                       'Výsledok 2. polčasu':'1X2',
                       'Výsledok zápasu bez remízy':'Víťaz zápasu bez remízy',
                       'Výsledok 1. polčasu bez remízy':'Víťaz zápasu bez remízy',
                       'Výsledok 2. polčasu bez remízy':'Víťaz zápasu bez remízy',
                       'Počet gólov v zápase':'Počet gólov',
                       'Počet gólov tímu v zápase':'Počet gólov',
                       'Počet gólov v 1. polčase':'Počet gólov',
                       'Počet gólov v 2. polčase':'Počet gólov',
                       'Počet gólov tímu v 1. polčase':'Počet gólov',
                       'Počet gólov tímu v 2. polčase':'Počet gólov',
                       'Handicap v zápase':'Handicap',
                       'Kto dá v zápase':'1. gól',
                       'Každý tím dá v zápase':'Každý tím dá 1 a viac gólov',
                       'Každý tím dá v 1. polčase':'Každý tím dá 1 a viac gólov',
                       'V ktorom polčase padne najviac gólov':'V ktorom polčase padne najviac gólov',
                       'Kto bude kopať v zápase':'Kto bude kopať v zápase 1. roh',
                       'Viac rohov v zápase':'Viac rohov v zápase',
                       'Počet rohov v zápase':'Počet rohov',
                       'Počet rohov v 1. polčase':'Počet rohov',
                       'Počet rohov v 2. polčase':'Počet rohov',
                       'Počet rohov tímu v zápase':'Počet rohov',
                       'Počet rohov tímu v 1. polčase':'Počet rohov',
                       'Počet rohov tímu v 2. polčase':'Počet rohov',
                       'Počet penált v zápase':'Penalta v zápase',
                       'Počet striel na bránu v zápase':'Počet striel na bránu',
                       'Počet faulov v zápase':'Počet faulov',
                       'Tím vyhrá aspoň jeden polčas':'Tím vyhrá aspoň jeden polčas',
                       'Tím vyhrá obidva polčasy':'Tím vyhrá obidva polčasy',
                       'Tím dá gól v oboch polčasoch':'Tím dá gól v oboch polčasoch'
}
potrebujem_tipsport = ['Výsledok zápasu',
                       'Výsledok 1. polčasu',
                       'Výsledok 2. polčasu',
                       'Výsledok zápasu bez remízy',
                       'Výsledok 1. polčasu bez remízy',
                       'Výsledok 2. polčasu bez remízy',
                       'Počet gólov v zápase',
                       'Počet gólov tímu v zápase',
                       'Počet gólov v 1. polčase',
                       'Počet gólov v 2. polčase',
                       'Počet gólov tímu v 1. polčase',
                       'Počet gólov tímu v 2. polčase',
                       'Handicap v zápase',
                       'Kto dá v zápase',
                       'Každý tím dá v zápase',
                       'Každý tím dá v 1. polčase',
                       'V ktorom polčase padne najviac gólov',
                       'Kto bude kopať v zápase',
                       'Viac rohov v zápase',
                       'Počet rohov v zápase',
                       'Počet rohov v 1. polčase',
                       'Počet rohov v 2. polčase',
                       'Počet rohov tímu v zápase',
                       'Počet rohov tímu v 1. polčase',
                       'Počet rohov tímu v 2. polčase',
                       'Počet penált v zápase',
                       'Počet striel na bránu v zápase',
                       'Počet faulov v zápase',
                       'Tím vyhrá aspoň jeden polčas',
                       'Tím vyhrá obidva polčasy',
                       'Tím dá gól v oboch polčasoch'

]

first_halftime = ['1.polčas','1. polčas','1.pol','1. pol']
second_halftime = ['2.polčas','2. polčas','2.pol','2. pol']
slovnik_nike_futbal = {'':'not found',
                        '1. polčas':'1X2',
                       'Zápas':'1X2',
                       '2. polčas':'1X2',
                       'Stávka bez remízy':'Víťaz zápasu bez remízy',
                       '1. polčas stávka bez remízy':'Víťaz zápasu bez remízy',
                       '2. polčas stávka bez remízy.':'Víťaz zápasu bez remízy',
                       '2. polčas stávka bez remízy':'Víťaz zápasu bez remízy',
                       'Počet gólov v zápase':'Počet gólov',
                       'jednotka počet gólov':'Počet gólov',
                       'dvojka počet gólov':'Počet gólov',
                       'Handicap':'Handicap',
                       '1. polčas počet gólov':'Počet gólov',
                       '2. polčas počet gólov':'Počet gólov',
                       '1.polčas počet gólov jednotka':'Počet gólov',
                       '1.polčas počet gólov dvojka':'Počet gólov',
                       '2.polčas počet gólov jednotka':'Počet gólov',
                       '2.polčas počet gólov dvojka':'Počet gólov',
                       '1. gól':'1. gól',
                       'Obaja dajú gól':'Každý tím dá 1 a viac gólov',
                       'Obaja dajú gól v 1.polčase':'Každý tím dá 1 a viac gólov',
                       'Polčas s viac gólmi':'V ktorom polčase padne najviac gólov',
                       '1.roh':'Kto bude kopať v zápase 1. roh',
                       'Viac rohov':'Viac rohov v zápase',
                       'Počet rohov':'Počet rohov',
                       'Počet rohov 1.pol.':'Počet rohov',
                       'Počet rohov jednotka':'Počet rohov',
                       'Počet rohov dvojka':'Počet rohov',
                       'Poč.rohov jednotka 1.pol.':'Počet rohov',
                       'Poč.rohov dvojka 1.pol.':'Počet rohov',
                       'Penalta v zápase':'Penalta v zápase',
                       'Strely na bránu':'Počet striel na bránu',
                       'Počet faulov':'Počet faulov',
                       'jednotka vyhrá aspoň jeden polčas':'Tím vyhrá aspoň jeden polčas',
                       'dvojka vyhrá aspoň jeden polčas':'Tím vyhrá aspoň jeden polčas',
                       'jednotka vyhrá každý polčas':'Tím vyhrá obidva polčasy',
                       'dvojka vyhrá každý polčas':'Tím vyhrá obidva polčasy',
                       'jednotka dá gól v každom polčase':'Tím dá gól v oboch polčasoch',
                       'dvojka dá gól v každom polčase':'Tím dá gól v oboch polčasoch'
}

potrebujem_nike = ['1. polčas',
                   'Zápas',
                   '2. polčas',
                   'Stávka bez remízy',
                   '1. polčas stávka bez remízy',
                   '2. polčas stávka bez remízy.',
                   '2. polčas stávka bez remízy',
                   'Počet gólov v zápase',
                   'jednotka počet gólov',
                   'dvojka počet gólov',
                   '1. polčas počet gólov',
                   '2. polčas počet gólov',
                   '1.polčas počet gólov jednotka',
                   '1.polčas počet gólov dvojka',
                   '2.polčas počet gólov jednotka',
                   '2.polčas počet gólov dvojka',
                   'Handicap',
                   '1. gól',
                   'Obaja dajú gól',
                   'Obaja dajú gól v 1.polčase',
                   'Polčas s viac gólmi',
                   '1.roh',
                   'Viac rohov',
                   'Počet rohov',
                   'Počet rohov 1.pol.',
                   'Počet rohov jednotka',
                   'Počet rohov dvojka',
                   'Poč.rohov jednotka 1.pol.',
                   'Poč.rohov dvojka 1.pol.',
                   'Penalta v zápase',
                   'Strely na bránu',
                   'Počet faulov',
                   'jednotka vyhrá aspoň jeden polčas',
                   'dvojka vyhrá aspoň jeden polčas',
                   'jednotka vyhrá každý polčas',
                   'dvojka vyhrá každý polčas',
                   'jednotka dá gól v každom polčase',
                   'dvojka dá gól v každom polčase'
]

slovnik_fortuna_futbal = {'':'not found',
                        'Výsledok 1. polčasu':'1X2',
                       'Zápas':'1X2',
                       '2.polčas':'1X2',
                       'Výsledok zápasu bez remízy':'Víťaz zápasu bez remízy',
                       'Počet gólov':'Počet gólov',
                       'jednotka počet gólov':'Počet gólov',
                       'dvojka počet gólov':'Počet gólov',
                       'Handicap':'Handicap',
                       'Počet gólov v 1. polčase':'Počet gólov',
                       '2.polčas počet gólov':'Počet gólov',
                       '1.polčas: jednotka počet gólov':'Počet gólov',
                       '1.polčas: dvojka počet gólov':'Počet gólov',
                       '2.polčas: jednotka počet gólov' : 'Počet gólov',
                       '2.polčas: dvojka počet gólov' : 'Počet gólov',
                       '1. gól':'1. gól',
                       'Každý z tímov dá gól':'Každý tím dá 1 a viac gólov',
                       '1.polčas: oba tímy dajú gól':'Každý tím dá 1 a viac gólov',
                       'Polčas s najvyšším počtom gólov':'V ktorom polčase padne najviac gólov',
                       'jednotka vyhrá aspoň jeden polčas':'Tím vyhrá aspoň jeden polčas',
                       'dvojka vyhrá aspoň jeden polčas':'Tím vyhrá aspoň jeden polčas',
                       'jednotka vyhrá oba polčasy':'Tím vyhrá obidva polčasy',
                       'dvojka vyhrá oba polčasy':'Tím vyhrá obidva polčasy',
                       'jednotka dá gól v oboch polčasoch':'Tím dá gól v oboch polčasoch',
                       'dvojka dá gól v oboch polčasoch':'Tím dá gól v oboch polčasoch'
}

potrebujem_fortuna = ['Výsledok 1. polčasu',
                       'Zápas',
                       '2.polčas',
                       'Výsledok zápasu bez remízy',
                       'Počet gólov',
                       'jednotka počet gólov',
                       'dvojka počet gólov',
                       'Handicap',
                       'Počet gólov v 1. polčase',
                       '2.polčas počet gólov',
                       '1.polčas: jednotka počet gólov',
                       '1.polčas: dvojka počet gólov',
                       '2.polčas: jednotka počet gólov',
                       '2.polčas: dvojka počet gólov',
                       '1. gól',
                       'Každý z tímov dá gól',
                       '1.polčas: oba tímy dajú gól',
                       'Polčas s najvyšším počtom gólov',
                       'jednotka vyhrá aspoň jeden polčas',
                       'dvojka vyhrá aspoň jeden polčas',
                       'jednotka vyhrá oba polčasy',
                       'dvojka vyhrá oba polčasy',
                       'jednotka dá gól v oboch polčasoch',
                       'dvojka dá gól v oboch polčasoch'
]

#s = Service(driver_path)
chrome_options = Options()
chrome_options.add_argument('--window-size=1920,1080')  
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
#chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--start-fullscreen')

if __name__ == '__main__':
    day = int(sys.argv[1])
    if(day==1):
        endpoint = 'https://www.nike.sk/tipovanie/futbal?zajtra'
        endpoint_tipsport = 'https://www.tipsport.sk/kurzy/futbal-16?timeFilter=form.period.tomorrow&limit=1000'
        endpoint_fortuna = f'https://www.ifortuna.sk/stavkovanie/futbal?selectDates=1&date={tomorrow}'
    while(True):
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(endpoint)
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME,"boxes-inner-view")))
            print('wrapper found')
            wrapper = driver.find_element_by_class_name("boxes-inner-view")
            while True:
                try:
                    WebDriverWait(driver, 20).until(EC.element_to_be_clickable(wrapper.find_element_by_class_name('btn-primary')))
                    driver.execute_script("arguments[0].click();", wrapper.find_element_by_class_name('btn-primary'))
                except Exception as e:
                    break 
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME,"boxes-inner-view")))
            wrapper = driver.find_element_by_class_name("boxes-inner-view")
            leagues = wrapper.find_elements_by_class_name("bg-dark-futbal")
            print('leagues found')
            matches = []
            for league in leagues:
                rows_inside_league = league.find_elements_by_class_name("bet-view-prematch-row")
                for row in rows_inside_league:
                    try:
                        team = row.find_element_by_class_name('bets-opponents').text.replace('\n','')
                        team = team.replace('vs',' - ')
                        matches.append(team)
                    except:
                        continue
                    
            driver.quit()

            """ small_arrays = np.array_split(np.array(matches), 3)
            arrays = []
            for i in small_arrays:
                arrays.append(i.tolist()) """
                
            threadLocal = threading.local()

            number_of_processes = min(4, len(matches))
            with ThreadPool(processes=number_of_processes) as pool:
                result_array = pool.map(check_multithread, matches)
                # Must ensure drivers are quitted before threads are destroyed:
                del threadLocal
                # This should ensure that the __del__ method is run on class Driver:
                gc.collect()

                pool.close()
                pool.join()
        except Exception as e:
            print(f'START {e}')
            pass