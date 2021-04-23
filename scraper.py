import prova
from selenium import webdriver
from controller.HTMLanalyzer import *
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
from urllib.parse import urlparse
import time
from controller.CSSanalyzer import * 
from controller.Downloader import *
from model.webpageInfo import *
from selenium.common.exceptions import WebDriverException

def web_scraper(url,loadingtime,safetytime):
    #inizio fase di analisi
    print("Web scraping analyisis")
    urls=[]
    urls.append(url)
    #variabile che rappresenta l'eventuale stato di loop che ha il programma 
    loop =False
    #installazione driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    #controllo della lingua per eventuale traduzione dei tasti next e previous per la pagination
    #language = driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
    #print(language)
    #translatedNext =
    #translatedPrevious =
    c=1
    #attributo che simboleggia il go back 1 volta per sito web
    firstTime=True
    #attributo che evita che il sito venga nuovamente scaricato se è stato già trovato 
    download =True
    for url in urls:
        #misurazione dei tempi
        start_time = time.time()
        htmlanalyzer = HTMLanalyzer()
        cssanalyzer = CSSanalyzer()
        downloader = Downloader()
        #set url,set id
        webPageInfo = WebpageInfo()
        #richiesta al sito web effettuare controllo
        #controllo che il sito web sia diverso per effettuare il goback
        parsedURL = urlparse(url)
        netloc = parsedURL.netloc
        scheme =parsedURL.scheme
        path = parsedURL.path
        par = parsedURL.params
        shorterLink =scheme+"://"+netloc
        urlLen= len(shorterLink)
        if loop==False:
            try:
                driver.get(url)
            except:
                print("Controlla la connessione internet")
        else:
            download=True
            loop=False
            #controlla
            firstTime=True
            c=c+1
            continue
        #rendere il driver non minimizzabile o perde il focus e non prosegue
        #driver.maximize_window()
        print(len(str(driver.page_source)))

        #metodo che scrolla dinamicamente la pagina fino al suo termine
        htmlanalyzer.scroll(driver,loadingtime,safetytime)
        #inizializzo nuovamente le variabili 
        resourceFound=set()
        previousHrefs=[]
        nextHrefs=[]
        moreHrefs=[]
        print("resfound",len(resourceFound))
        print("resfound",len(webPageInfo.getResources()))
        
        #metodo che analizza la pagina html estrapolando gli src e gli href dai tag considerati sensibili e anche gli alt ed eventualmente test migliorabile
        resourceFound,previousHrefs,nextHrefs,moreHrefs,sheets = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")
        print(firstTime)
        
        #funzione che torna indietro il piu possibile ed effettua in caso una nuova ricerca delle risorse html
        if firstTime:
            print(previousHrefs)
            xpath = htmlanalyzer.findGoBack(driver,previousHrefs)
            print(xpath)
            if xpath!=False and xpath!="NoElements":
                print(c)
                urls.insert(c,str(driver.current_url))
                print(urls)
                c=c+1
                firstTime=True
                continue
            else:
                firstTime = False
            """out = htmlanalyzer.goBack(driver,previousHrefs)
            print("out",out)
            if(out == "research"):
                resourceFound=set()
                previousHrefs=[]
                nextHrefs=[]
                moreHrefs=[]
                resourceFound,previousHrefs,nextHrefs,moreHrefs,sheets = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")"""
        if download:
            #analisi del  css
            #metodo che nella pagina html cerca i tag link contenenti css  
            print(sheets)
            if(len(sheets)> 0):
                #per ogni link trovato
                for sheetURL in sheets:
                    print(sheetURL)
                    #metodo che cerca gli url nelle classi css e li inserisce in un set
                    webPageInfo.extendResources(cssanalyzer.cssParser(sheetURL,url))
                    print("---------------------------------------------------------------------\n")
                print(len(webPageInfo.getResources()))       
            else:
                print("css not found")
            #join set() css e html
            webPageInfo.extendResources(resourceFound)
            print("---------------------------------------------------------------------\n")
            #webPageInfo.printResources()
            counter=1
            resources = webPageInfo.getResources()
            print(len(resources))
            #se il sito è uguale al precedente non scaricare
            srcFolder = downloader.mkDirForUrl(url,c)
            for resource in resources:
                try:
                    #metodo che dato il set di risorse le scarica nel formato "corretto" migliorabile
                    result=downloader.resourcesDown(resource,counter,srcFolder)
                    counter = counter+1
                except:
                    print("not downloadable")
            #se la pagina è la stessa altrimenti append
            docFileName = url.split('/')
            webPageInfo.toCSV(netloc+str(c),start_time,docFileName[2],url)
            webPageInfo.appendToDataset(netloc)
        download=True    
        #funzione che  va avanti il piu possibile 
        print(nextHrefs)
        xpath = htmlanalyzer.findGoNext(driver,nextHrefs)
        print(xpath)
        if xpath!=None and xpath!="NoElements":
            print( "Elemento cliccato,aggiungendo un 'altra sub page agli url da cercare")
            print(str(driver.current_url))
            print(c)
            urls.insert(c,str(driver.current_url))
            print(urls)
            time.sleep(2)
            firstTime=False
            #fix
            if url == driver.current_url:
                download=False
                #se l'elemento precedente è anche uguale vuol dire che sta andando in loop dunque se possibile proseguire con un altro url
                if urls[c-2] == url:
                    loop =True
                    firstTime=True
        #funzione che  va avanti il piu possibile 
        c=c+1
        webPageInfo.clearResources()
    driver.close()
    return urls





#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#import urls e id

current_dir=os.getcwd()
urls,urlsID = Utils().getCSVfromdir(current_dir,"Master.csv")
print(urls)
print(urlsID)
if not urls or not urlsID:
    print("urls are empty or id empty")
    os._exit(0)
#urls=['https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3']
#https://it.xhamster.com/3 #'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''
#tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
safetytime = 60
#tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
loadingtime = 7

for url in urls:
    web_scraper(url,loadingtime,safetytime)
        
            
            
        
        
        
        
        
