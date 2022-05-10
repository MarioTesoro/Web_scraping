import imaplib                              #librerie per poter gestire le email
import email                                ################
from email.header import decode_header      ############
from datetime import datetime, timedelta    #libreria per gestire le date
import re                                   #libreria per la ricerca di URL nelle stringhe
from ReportManagement import WritingOnCsv                         #libreria per scrittura di dati su csv
from decouple import config                 #libreria per prendere dati sensibili da file .env
from Model.Email import Email               #classe model per email

#tipo di email a cui accedere
host = 'imap.gmail.com'

#metodo che si occupa di trovare gli URL all'interno di una stringa
def find(string):
    #confronta regex, path generico dell'URL, con la stringa in input 
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)
    #restituisce tutti gli Url trovati      
    return [x[0] for x in url]

        
#metodo che si occupa di accedere alla proprio email e estrarre le informazioni necessarie come corpo dell'email
#data dell'email, ecc.
def get_inbox(username,password):
    #qui avviene la connessione con la mail box
    mail = imaplib.IMAP4_SSL(host)
    try:
        mail.login(username, password)
    except:
        return False
    mail.select("inbox")
    #qui viene calcolata la data relativa a 7 giorni prima di quella odierna
    #in modo tale che possano essere considerate solo le email della settimana corrente
    date = (datetime.today() - timedelta(7)).strftime("%d-%b-%Y")
    #nella mail box vengono estratte solo le email che hanno come oggetto 'segnalazione' e che
    #sono massimo di una settimana prima al giorno corrente
    _, search_data = mail.search(None, '(SENTSINCE {date})'.format(date=date))

    #successivamente poi vengono estratti i dati relativi ad ogni email che ha
    #le caratteristiche sopra indicate
    my_message = []
    for num in search_data[0].split():
        email_data = {}
        _, data = mail.fetch(num, '(RFC822)')
        _, b = data[0]
        #vengono effettuate le dovute conversioni
        email_message = email.message_from_bytes(b)
        for header in ['subject', 'to', 'from', 'date']:
            email_data[header] = email_message[header]
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True)
                email_data['body'] = body.decode()
        my_message.append(email_data)
    #e vi è un return di un dictionary contenente le informazioni di ogni email
    #estratta
    return my_message

#metodo che si occupa di scrivere gli Url trovati nelle email
#all'interno del file .csv
def transferFromEmail():
    urls = []
    email = config('EMAIL')
    password = config('EMAILPASSWORD')
    #qui viene chiamato il metodo che accede all'email e prende le informazioni necessarie dalle email corrette
    #una volta prelevate vengono cancellate le stringhe di email e password, per questioni di sicurezza
    #in modo tale che rimangano il meno tempo possibile in memoria
    my_inbox = get_inbox(email,password)
    del email,password
    #se il login è stato effettuato con successo
    if type(my_inbox) != bool:
        #per ogni email che abbiamo trovato, viene prelevato l'url dal corpo della mail
        email_info = []
        urls = []
        for email in my_inbox:
            email_obj = Email()
            temporary_urls = find(email['body'])
            for url in urls:
                try:
                     temporary_urls.remove(url)
                except ValueError:
                     pass 
            email_obj.set_sender(email['from'])
            email_obj.set_urls(temporary_urls)
            email_info.append(email_obj)
            urls.extend(temporary_urls)
            #e viene controllato che non ci siano url duplicati, in tal caso, ne viene lasciato solo uno
            urls = list(dict.fromkeys(urls))
        return email_info
    #altrimenti, viene restituito True per fare capire che le credenziali erano errate
    else:
        return True
