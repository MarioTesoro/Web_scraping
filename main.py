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

#url = input("Type website url: ")
print("Web scraping analyisis")
#https://www.ansa.it/ #vanno accettati i cookies
urls=['https://it.xhamster.com/4']#'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''

downlaod_path = Utils().getDownloadPath()
print(downlaod_path)
try:
    driver = webdriver.Chrome(ChromeDriverManager().install())
except:
    print("Controlla la connessione internet")


#tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
safetytime = 30
#tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
loadingtime = 7
#controllo della lingua per eventuale traduzione dei tasti next e previous per la pagination
language = driver.execute_script("return window.navigator.userLanguage || window.navigator.language")
print(language)
#translatedNext =
#translatedPrevious =
c=1
for url in urls:
    htmlanalyzer = HTMLanalyzer()
    cssanalyzer = CSSanalyzer()
    downloader = Downloader()
    #set url,set id
    webPageInfo = WebpageInfo()
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
        htmlanalyzer.scroll(driver,loadingtime,safetytime)
        """
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
        """
        #metodo che analizza la pagina html estrapolando gli src e gli href dai tag considerati sensibili e anche gli alt ed eventualmente test migliorabile
        resourceFound,previousHrefs,nextHrefs,moreHrefs = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")
        print(previousHrefs)
        print(nextHrefs)
        print(moreHrefs)
        
        #funzione che torna indietro il piu possibile 
        result = htmlanalyzer.goBack(driver,previousHrefs)
        while result!=False:
            if result == "NoElements":
                print("NoElements")
                break
            try:
                selen_elem =driver.find_element_by_xpath(result)
                print(selen_elem)
                driver.execute_script("arguments[0].scrollIntoView();", selen_elem)
                selen_elem.click()
                print("click")
                time.sleep(5)
            except WebDriverException:
                print( "Elemento non più cliccabile")
                break
            
        
                
        """   
        parsedURL = Utils().parseUrl(url)
        cwd =os.getcwd()
        srcFolder =  cwd+ os.path.sep+"src"+os.path.sep
        hrefFolder = cwd + os.path.sep+"href"+os.path.sep
        if os.path.exists(srcFolder) and os.path.exists(hrefFolder):
            #join set() css e html
            print("---------------------------------------------------------------------\n")
            #webPageInfo.printResources()
            
            counter=1
            resources = webPageInfo.getResources()
            print(len(resources))
            
            for resource in resources:
                try:
                        #metodo che dato il set di risorse le scarica nel formato "corretto" migliorabile
                    result=downloader.resourcesDown(resource,counter,srcFolder,hrefFolder)
                    counter = counter+1
                    
                except:
                    print("exception")
        
            #se la pagina è la stessa altrimenti append
            webPageInfo.toCSV('csvFile'+str(c))
            c=c+1
        else:
            print("no existing directory")
        """
                
            
        
        
        """
        #funzione che prosegue fino all'ultima pagina disponibile
        result=True
        nextElem= None
        while result!=False:
            result = prova.pagination(driver,url,"goNext",nextElem)
            print(result)
            if result == "NoElements":
                print("controlla perchè non trova nessun elemento nella pagination")
                break
            nextElem=result
            print(nextElem)
            time.sleep(3)
        """
        
        
        
            
            
        
        
        
        
        
