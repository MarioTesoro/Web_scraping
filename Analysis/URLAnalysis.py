import requests                         #libreria per controlli sugli URL
from decouple import config             #libreria per prendere dati sensibili da file .env
import json                             #libreria per interagire con l'api
from Model.Malware import Malware       #classe model per prendere informazioni sui malware

#metodo utilizzato per accedere all'API IBM X-force Exchange
def access_Api(api_url,url_to_check):
     api_key= config('APIKEY')
     api_password = config('APIPASSWORD')
     response = requests.get(api_url + url_to_check, auth=(api_key, api_password))
     return response

#metodo utilizzato per il controllo preliminare sugli URL
#per verificare l'esistenza del sito, a prescindere dall'analisi 
#fatta con API
def check_url_stCode(url): 
    #qui viene fatta la richiesta al sito, se non va a buon fine
    #l'url non è valido e quindi viene restituito 0
    try:
        request = requests.get(url,allow_redirects=True)
        print(request)
    except: 
        return False
    #se invece va a buon fine, viene controllato il tipo di codice restituito:
    #200: l'url funziona
    #viene restituito 1, l'url è valido
    #429: la richiesta è stata effettuata troppe volte e il sito le ha bloccate
    #anche in questo caso l'url viene considerato valido
    #403: il sito non permette di richiamare l'URL, ma questo è corretto
    #302: necessario intervento umano, quindi redirect(es. richiesta di accettazione di alcune condizioni)
    #anche in questo caso l'url viene considerato valido
    stCode = request.status_code
    if stCode != 200:
         if stCode == 429 or stCode == 302 or stCode == 403:
             return True
         return False
    else:
         return True

#metodo utilizzato per accedere alla history del sito, tramite URL
#in modo particolare prendiamo la categoria e la sua descrizione
def check_URL_history(url,url_st_code):
    #viene effettuato prima l'accesso all'API
    api_url_history = 'https://api.xforce.ibmcloud.com/url/history/'
    response_history = access_Api(api_url_history,url)
    #controllato lo statuts code dell'url come controllo preliminare
    #se lo status code è uno tra quelli accettati
    if(url_st_code == True):
        #viene effettuata l'analisi dell'URL tramite API
        responseJson = response_history.json()
        #se l'API restituisce un'errore per quell'URL, ovvero non riesci a prelevare informazioni
        #ritorna il controllo al chiamante del metodo
        if responseJson.get('error') != None:
            return True, True
        #altrimenti recupera la categoria e la descrizione della categoria
        else:
            cats = responseJson['cats']
            category_name = ''
            category_data = {}
            for category in cats:
                category_data = cats[category]
                category_name = category
            return category_data['description'], category_name
    #se lo status code non è tra quelli accettati vuol dire che l'URL è errato
    else:
        return False,False

#metodo utilizzato per verificare la presenza di malware nel sito collegato allo specifico URL
def check_URL_malware(url):
    #viene effettuato prima l'accesso all'API
    api_url_malware = 'https://api.xforce.ibmcloud.com/url/malware/'
    response_malware = access_Api(api_url_malware,url)
    
    #viene effettuata l'analisi dell'URL tramite API
    responseJson = response_malware.json()
    #se l'API restituisce un'errore per quell'URL, ovvero non riesce a prelevare informazioni
    #ritorna il controllo al chiamante del metodo
    if responseJson.get('error') != None:
        return True, True
    else:
        #altrimenti preleva la lista di malware 
        malwares = responseJson['malware']
        #se non ce ne sono
        if not malwares:
            #restituisce il controllo al chiamante
            return True, True
        #altrimenti preleva le tipologie e le famiglie di Malware trovati,
        #il dominio, il filepath, l'ip
        #e il numero di malware presenti
        else:
            number_of_malwares = 0
            malware_info = []
            for malware in malwares:
                malware_obj = Malware()
                malware_obj.set_malware_type(malware['type'])
                malware_obj.set_family(malware['family'])
                malware_obj.set_domain(malware['domain'])
                malware_obj.set_filepath(malware['filepath'])
                malware_obj.set_ip(malware['ip'])
                malware_info.append(malware_obj)
                number_of_malwares += 1
            
            return malware_info, number_of_malwares
