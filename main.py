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



#misurazione dei tempi
start_time = time.time()
#import urls e id
current_dir=os.getcwd()
urls,urlsID = Utils().getCSVfromdir(current_dir,"input.csv")
print(urls)
print(urlsID)
#inizio fase di analisi
print("Web scraping analyisis")
#https://www.ansa.it/ #vanno accettati i cookies
urls=['https://it.xhamster.com/3']
#https://it.xhamster.com/3#'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
except:
    print("Controlla la connessione internet")


#tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
safetytime = 60
#tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
loadingtime = 7
#controllo della lingua per eventuale traduzione dei tasti next e previous per la pagination
language = driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
print(language)
#translatedNext =
#translatedPrevious =
c=1
#attributo che simboleggia il go back 1 volta per sito web
firstTime=True
download =True
for url in urls:
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
    driver.get(url)
    #rendere il driver non minimizzabile o perde il focus e non prosegue
    #driver.maximize_window()
    print(len(str(driver.page_source)))
    
   
    try: 
        print("")
    except Exception as e:
        print(e.__cause__)
    finally:
        print("")
        #chiusura driver
        #driver.close()
        #fine misurazione tempi e stampa per eventuali test
        print("--- %s seconds ---" % (time.time() - start_time))

        
        #metodo che scrolla dinamicamente la pagina fino al suo termine
        htmlanalyzer.scroll(driver,loadingtime,safetytime)
        
        #metodo che analizza la pagina html estrapolando gli src e gli href dai tag considerati sensibili e anche gli alt ed eventualmente test migliorabile
        resourceFound,previousHrefs,nextHrefs,moreHrefs = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")
        print(previousHrefs)
        print(nextHrefs)
        print(moreHrefs)
        print(firstTime)
        
        #funzione che torna indietro il piu possibile ed effettua in caso una nuova ricerca delle risorse html
        if firstTime:
            out = htmlanalyzer.goBack(driver,previousHrefs)
            print("out",out)
            if(out == "research"):
                resourceFound=set()
                previousHrefs=[]
                nextHrefs=[]
                moreHrefs=[]
                resourceFound,previousHrefs,nextHrefs,moreHrefs = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")
        firstTime=True

        if download:
            
            #analisi del  css
            #metodo che nella pagina html cerca i tag link contenenti css migliorabile link[:3]== .css 
            sheets = cssanalyzer.findCssSheets(url,driver.page_source)
            print(sheets)
            
            if(len(sheets)> 0):
                #per ogni link trovato
                for sheetURL in sheets:
                    print(sheetURL)
                    #metodo che cerca gli url nelle classi css e li inserisce in un set
                    
                    webPageInfo.extendResources(cssanalyzer.cssParser(sheetURL,url))
                    print("---------------------------------------------------------------------\n")
                print(len(webPageInfo.getResources()))
                #webPageInfo.toCSV(1)
                #time.sleep(5)        
            else:
                print("css not found")
            #downlaod source code
            #funcs.sourceCodeDownloader(url,downlaod_path)
            
            #join set() css e html
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
            webPageInfo.toCSV(netloc+str(c))
            webPageInfo.appendToDataset(url)
        download=True
        
        
        #funzione che  va avanti il piu possibile 
        
       
        xpath = htmlanalyzer.findGoNext(driver,nextHrefs)
        print(xpath)
        if xpath!=None or xpath!="NoElements":
            print( "Elemento cliccato,aggiungendo un 'altra sub page agli url da cercare")
            print(str(driver.current_url))
            try:
                #trova l'ultima occorrenza di quel sito 
                index=''.join(urls).rindex(url)
            except:
                #altrimenti aggiungilo nella posizione immediatamente successiva a questa
                index =urls.index(url)
            #trova l'indice dell' ultima occorrenza e non della prima

            urls.insert(index+1,str(driver.current_url))
            print(urls)
            time.sleep(2)
            firstTime=False
            if url == driver.current_url:
                download=False
        #funzione che  va avanti il piu possibile 
        c=c+1
        webPageInfo.clearResources()
        
                

      
        
        
            
            
        
        
        
        
        
