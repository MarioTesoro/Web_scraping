import os                                #libreria per interagire con il SO
import csv                               #libreria per gestire i CSV
from Analysis import URLAnalysis                       #libreria per analizzare gli URL acquisiti
from Model.Malware import Malware        #classe model per prendere informazioni sui malware
from datetime import datetime            #libreria per gestire la data
from Model.WhoisRecord import Whois      #classe model per record whois
from Analysis import TakeWhois                         #necessario per prendere informazioni sull'URL
from ReportManagement import WriteReport

#spazi vuoti per le informazioni dei malware
empty_space = '############'
#formato della data
date_format = '%Y-%m-%d'

#metodo per scrivere su un file Csv esistente
def writingExistingCsv(csvFile,urls,creds):
    numberOfRows = 1
    #il file viene aperto in lettura per recuperare il numero di righe utile per ID
    #se il file è aperto sul computer non ci si puo interagire quindi restituisce un errore
    try:
        r_out_f = open(csvFile ,'r',encoding='utf-8') 
    except:
        return False
    reader = csv.reader(r_out_f, delimiter=';')
    #qui viene saltata la prima riga, ovvero l'header del file
    next(reader)
    #qui estratti gli Url già presenti nel file
    #e il numero di righe presenti
    listofExistingsite = []
    splitted_existing_urls = []
    count = 0
    for rows in reader:
         if(rows[3] != ''):
             listofExistingsite.append(rows[3])
             numberOfRows += 1
    count = numberOfRows
    for existing_site in listofExistingsite:
        temporary = existing_site.split('/')
        splitted_existing_urls.append(temporary[2])
    #qui vengono poi aggiunti tutti i nuovi URL al file .csv
    #se il file è aperto sul computer non ci si puo interagire quindi restituisce un errore
    try:
        out_f = open(csvFile ,'a', newline='',encoding="utf-8") 
    except:
        return False
    writer = csv.writer(out_f, delimiter=';')
    for url in urls:
        url_splitted = url.split('/')
        #controllando anche che gli url appena ricevuto non siano
        #già memorizzati, in tal caso non verranno scritti
        if url_splitted[2] not in splitted_existing_urls:
            writeURL(url,numberOfRows,writer,creds)
            numberOfRows+=1
    #se il numero di righe nel file è rimasto invariato, vuol dire che gli url erano già presenti
    #quindi viene ritornato uno stato utile per mostrare un errore
    if count == numberOfRows:
        r_out_f.close()
        return 'alreadyIn'
    r_out_f.close()

#metodo per scrivere su un file Csv nuovo
def writingNewCsv(csvFile,urls,creds):
    numberOfRows = 1
    #apre il file csv in scrittura, se non esiste lo crea
    #e scrive tutti gli URL
    #se il file è aperto sul computer non ci si puo interagire quindi restituisce un errore
    try: 
        out_f = open(csvFile ,'w', newline='',encoding="utf-8") 
    except:
        return False
    writer = csv.writer(out_f, delimiter=';')
    writer.writerow(['ID','Data','Provenienza','URL','Esito','Categorie','Dominio','Creato','Aggiornato','Scadenza','Nome del registrante',
                     'Organizzazione registrante','Città e/o regione del registrante','Nome Registrar','Email',
                     'Numero di Malware Trovati','','','','Tipologia di Malware','Famiglie del Malware','Dominio','FilePath','IP'])
    for url in urls:
        writeURL(url,numberOfRows,writer,creds)
        numberOfRows+=1
    out_f.close()

#metodo che in base a se il file Master già esiste o no, scrive su di essi
def writingIntoCsv(csvFile,urls,creds):
    #qui viene controllato se il file .csv già esiste
    #se è così viene aperto in lettura e poi in append, per aggiungere le informazioni
    #altrimenti viene creato un nuovo file
    if os.path.isfile(csvFile):
        status_code = writingExistingCsv(csvFile,urls,creds)
        #se lo status code è False, c'è stato un problema durante l'apertura del file
        if  status_code == False:
            return False
        #altrimenti, se lo status code è uguale ad alreadyIn, gli URL erano stati già inseriti    
        elif status_code == 'alreadyIn':
            return 'alreadyIn'
    else: 
        status_code = writingNewCsv(csvFile,urls,creds) 
        if status_code == False:
            return False
    return True

def write_malware(malware_info,writer):
    malware_obj = Malware()
    for i in range(len(malware_info)):
         malware_obj = malware_info[i]
         writer.writerow(['','','','','','','','','','','','','','','','','','','',
                         str(malware_obj.get_malware_type()),str(malware_obj.get_family()),str(malware_obj.get_domain()),
                         str(malware_obj.get_filepath()),str(malware_obj.get_ip())])

def writeURL(url,numberOfRows,writer,creds):
    #per ogni URL viene effettuata l'analisi della history per ottenere categoria e Descrizione categoria del sito
    category_description, category_type = URLAnalysis.check_URL_history(url,URLAnalysis.check_url_stCode(url))
    #se la categoria è uguale False, allora l'URL è errato
    if(category_type == False):
        writer.writerow([numberOfRows,datetime.today().strftime(date_format),creds,url,'Non Corretto','','','','','','','','','','',
                         '','','','', empty_space, empty_space, empty_space, empty_space, empty_space])
    #altrimenti vuol dire che l'URL è corretto e procede con i controlli da API
    else:
        #continua allora controllando se ci sono malware
        malware_info, malware_number = URLAnalysis.check_URL_malware(url)
        #e acquisisce il record Whois, come informazioni di dominio dell'URL
        whois_obj = Whois()
        whois_obj = TakeWhois.take_whois_record(url)
        WriteReport.write_report(url, whois_obj, malware_info, malware_number, category_type, category_description)
        #se i malware ci sono e ha trovato anche la categoria con relativa descrizione
        #scrive categoria, descrizione, record whois e tipo, famiglia e numero di malware all'interno del csv
        if(malware_info != True and category_type != True):
             writer.writerow([numberOfRows,datetime.today().strftime(date_format),creds,url,'Corretto',
                             str(category_type)+': '+str(category_description),str(whois_obj.get_domain()),str(whois_obj.get_creation_date()),
                             str(whois_obj.get_updated_date()),str(whois_obj.get_expiration_date()),str(whois_obj.get_name()),
                             str(whois_obj.get_org()),str(whois_obj.get_location()),str(whois_obj.get_registrar()),str(whois_obj.get_email()),
                              malware_number,'','','', empty_space, empty_space, empty_space, empty_space, empty_space])
             write_malware(malware_info,writer)
             
        #altrimenti se non ha trovato malware, ma solo le informazioni della categoria, scrive le informazioni relative alla categoria e
        #record whois
        elif(malware_info == True and category_type != True):
             writer.writerow([numberOfRows,datetime.today().strftime(date_format),creds,url,'Corretto',
                             str(category_type)+': '+str(category_description),str(whois_obj.get_domain()),str(whois_obj.get_creation_date()),
                             str(whois_obj.get_updated_date()),str(whois_obj.get_expiration_date()),str(whois_obj.get_name()),
                             str(whois_obj.get_org()),str(whois_obj.get_location()),str(whois_obj.get_registrar()),str(whois_obj.get_email()),
                             '0','','','', empty_space, empty_space, empty_space, empty_space, empty_space])
        #altrimenti se ha trovato malware ma nessuna informazione sulla categoria, scrive solo le informazioni dei malware e
        #record whois
        elif(malware_info != True and category_type == True):
             writer.writerow([numberOfRows,datetime.today().strftime(date_format),creds,url,'Corretto','',str(whois_obj.get_domain()),
                             str(whois_obj.get_creation_date()),str(whois_obj.get_updated_date()),str(whois_obj.get_expiration_date()),
                             str(whois_obj.get_name()),str(whois_obj.get_org()),str(whois_obj.get_location()),str(whois_obj.get_registrar()),
                             str(whois_obj.get_email()),malware_number,'','','', empty_space, empty_space, empty_space, empty_space, empty_space])
             write_malware(malware_info,writer)
        #altrimenti se non ha trovato nulla, non scrive niente, tranne il record whois e che l'URL è corretto
        else:
             writer.writerow([numberOfRows,datetime.today().strftime(date_format),creds,url,'Corretto','',str(whois_obj.get_domain()),
                             str(whois_obj.get_creation_date()),str(whois_obj.get_updated_date()),str(whois_obj.get_expiration_date()),
                             str(whois_obj.get_name()),str(whois_obj.get_org()),str(whois_obj.get_location()),str(whois_obj.get_registrar()),
                             str(whois_obj.get_email()),'0','','','', empty_space, empty_space, empty_space, empty_space, empty_space])