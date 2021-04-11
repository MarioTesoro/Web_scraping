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
import json

def toCSV(setName,filename):
        numberOfRows = 1
        
        with open(Utils().getDownloadPath()+os.path.sep+ str(filename)+'.csv' ,'w', newline='') as out_f:
            writer = csv.writer(out_f, delimiter=';')
            writer.writerow(['ID','URL','NOME FILE','NOME ATTUALE','TESTO ALT','TESTO NEL TAG','FORMATO','STATUS'])
            for res in setName:
                r = Resource()
                r = res
                writer.writerow([numberOfRows,r.getUrl(),r.getFileName(),r.getNewFilename(),r.getAlt(),r.getText(),r.getFormat(),r.getStatus()])
                numberOfRows+=1 

#misurazione dei tempi
start_time = time.time()

#url = input("Type website url: ")
print("Web scraping analyisis")
#https://www.ansa.it/ #vanno accettati i cookies
urls=['https://www.ansa.it/']#'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''

downlaod_path = Utils().getDownloadPath()
print(downlaod_path)
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
except:
    print("Controlla la connessione internet")


#tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
safetytime = 30
#tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
loadingtime = 10
for url in urls:
    htmlanalyzer = HTMLanalyzer()
    cssanalyzer = CSSanalyzer()
    downloader = Downloader()
    webPageInfo = WebpageInfo()
    #urlPath= urlparse(url)
    #print(urlPath)
    #richiesta al sito web effettuare controllo
    driver.get(url)#check if driver
    driver.maximize_window()
    print(len(str(driver.page_source)))
    
   
    try: 
        print("ciao")
    except Exception as e:
        print(e.__cause__)
    finally:
        print("end")
        #chiusura driver
        #driver.close()
        #fine misurazione tempi e stampa per eventuali test
        print("--- %s seconds ---" % (time.time() - start_time))


        #metodo che scrolla dinamicamente la pagina fino al suo termine
        htmlanalyzer.scroll(driver,10,30)
        page = driver.page_source
        #result =prova.pagination(driver,urlPath)
        #print(result)
        #metodo che nella pagina html cerca i tag link contenenti css migliorabile link[:3]== .css 
        
        sheets = cssanalyzer.findCssSheets(url,page)
        print(sheets)
        
        if(len(sheets)> 0):
            #per ogni link trovato
            c=1
            for sheetURL in sheets:
                print(sheetURL)
                #metodo che cerca gli url nelle classi css e li inserisce in un set
                
                webPageInfo.extendResources(cssanalyzer.cssParser(sheetURL,url))
                print("---------------------------------------------------------------------\n")
            print(len(webPageInfo.getResources()))
            #webPageInfo.toCSV(1)
            time.sleep(5)
                
        else:
            print("css not found")
        
        #downlaod source code
        #funcs.sourceCodeDownloader(url,downlaod_path)
        #metodo che analizza la pagina html estrapolando gli src e gli href dai tag considerati sensibili e anche gli alt ed eventualmente test migliorabile
        resourceFound = htmlanalyzer.resourceFinder(page,url)
        print(len(resourceFound))
        #join set() css e html
        print("---------------------------------------------------------------------\n")
        #webPageInfo.printResources()
        counter=1
        resources = webPageInfo.getResources()
        print(len(resources))
    
        for resource in resources:
            try:
                    #metodo che dato il set di risorse le scarica nel formato "corretto" migliorabile
                result=downloader.resourcesDown(resource,counter)
                counter = counter+1
                
            except:
                print("exception")
    
        #se la pagina è la stessa altrimenti append
        webPageInfo.toCSV('csvFile')
        
        
        
        
        
