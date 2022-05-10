import whois                            #libreria per effettuare richiesta di record whois su un determinato URL
from datetime import datetime           #libreria per gestire la data
from Model.WhoisRecord import Whois     #classe model per gestire le informazioni record whois

#formato della data
date_format = '%d-%m-%Y'
#oggetto per record whois
whois_obj = Whois()

#metodo che si occupa di recuperare le informazioni su un determinato dominio, tramite URL
def take_whois_record(url):
    #effettua la query di tipo whois, per ottenere informazion sul dominio dell'URL
    response = whois.whois(url)
    #qui viene prelevato il nome del domnio
    #che in alcuni casi può essere prelvato in due modi
    #tutto maiuscolo o tutto minuscolo
    #qui viene preso sempre tutto minuscolo
    domain_name = response['domain_name']
    if domain_name!=None:
        if type(domain_name) == list:
            whois_obj.set_domain(domain_name[1])
        else:
            whois_obj.set_domain(domain_name)

    #qui viene prelevata la data di creazione
    #se più di una preleva l'ultima
    creation_date = response['creation_date']
    if creation_date!=None:
        if type(creation_date) == list:
            whois_obj.set_creation_date(creation_date[len(creation_date)-1].strftime(date_format))
        else:
            whois_obj.set_creation_date(creation_date.strftime(date_format))

    #qui viene prelevata l'ultima data di aggiornamento, nel momento in cui fosse più di una
    updated_date = response['updated_date']
    if updated_date!=None:
        if type(updated_date) == list:
            whois_obj.set_updated_date(updated_date[len(updated_date)-1].strftime(date_format))
        else:
            whois_obj.set_updated_date(updated_date.strftime(date_format))

    #qui viene prelevata la data di scadenza
    expiration_date = response['expiration_date']
    if expiration_date!=None:
        if type(expiration_date) == list:
            whois_obj.set_expiration_date(expiration_date[len(expiration_date)-1].strftime(date_format))
        else:
            whois_obj.set_expiration_date(expiration_date.strftime(date_format))
    #poi vengono prelevati: nome, organizzazione, città e regione,registrar e le email associate
    #con opportuni controlli sui campi del dictionary
    
    #queste tre suddivisioni in funzioni sono state fatte per aumentare la qualità dettata da sonarCloud
    check_whois_name(response)

    check_whois_location(response)

    check_whois_organization(response)

    if 'org' in response:
        whois_obj.set_org(response['org'])
    elif 'admin_organization' in response:
        whois_obj.set_org(response['admin_organization'])
    elif 'tech_organization' in response:
        whois_obj.set_org(response['tech_organization'])
    else:
        whois_obj.set_org('None')

    

    whois_obj.set_registrar(response['registrar'])
    if 'emails' in response:
        whois_obj.set_email(response['emails'])
    else:
        whois_obj.set_email('None')

    return whois_obj

def check_whois_location(response):
    if 'city' in response and 'state' in response:
        whois_obj.set_location(str(response['city'])+', '+str(response['state']))
    elif 'city' in response and 'state' not in response:
        whois_obj.set_location(str(response['city']))
    elif 'city' not in response and 'state' in response:
        whois_obj.set_location(str(response['state']))
    else:
        whois_obj.set_location('None, None')

def check_whois_name(response):
    if 'name' in response:
        whois_obj.set_name(response['name'])
    elif 'admin_name' in response:
        whois_obj.set_name(response['admin_name'])
    elif 'tech_name' in response:
        whois_obj.set_name(response['tech_name'])
    else:
        whois_obj.set_name('None')

def check_whois_organization(response):
    if 'org' in response:
        whois_obj.set_org(response['org'])
    elif 'admin_organization' in response:
        whois_obj.set_org(response['admin_organization'])
    elif 'tech_organization' in response:
        whois_obj.set_org(response['tech_organization'])
    else:
        whois_obj.set_org('None')