import funcs
import prova
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
from urllib.parse import urlparse
import time



#misurazione dei tempi
start_time = time.time()

#url = input("Type website url: ")
print("Web scraping analyisis")
#https://www.ansa.it/ #vanno accettati i cookies
urls=['https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3']#'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''

#downlaod_path = funcs.getDownloadPath()
#print(downlaod_path)
driver = webdriver.Chrome(ChromeDriverManager().install())

for url in urls:
    cssURLS= set()
    htmlURLS = set()
    alts = set()
    urlPath= urlparse(url)
    print(urlPath)
    #richiesta al sito web effettuare controllo
    driver.get(url)
    driver.maximize_window()
    print(len(str(driver.page_source)))
    try:
        element = driver.find_element_by_tag_name('body')
        #tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
        safetytime = 30 
        #tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
        loadingTime= 10
        #metodo che scrolla dinamicamente la pagina fino al suo termine
        funcs.scroll(driver,loadingTime,safetytime)
        page = driver.page_source
        #result =prova.pagination(driver,urlPath)
        #print(result)
        #metodo che nella pagina html cerca i tag link contenenti css migliorabile link[:3]== .css 
        sheets = funcs.findCssSheets(url,page)
        print(sheets)
        
        if(len(sheets)> 0):
            #per ogni link trovato
            for sheetURL in sheets:
                print(sheetURL)
                #metodo che cerca gli url nelle classi css e li inserisce in un set
                cssURLS.update(funcs.cssParser(sheetURL,url)) 
                print("---------------------------------------------------------------------\n")
            print(cssURLS)
        else:
            print("css not found")
        
        #downlaod source code
        #funcs.sourceCodeDownloader(url,downlaod_path)
        #metodo che analizza la pagina html estrapolando gli src e gli href dai tag considerati sensibili e anche gli alt ed eventualmente test migliorabile
        htmlURLS,alts = prova.finder(page,url)
        #join set() css e html
        
        htmlURLS.update(cssURLS)
        print("---------------------------------------------------------------------\n")
        print(alts)
        counter=1
        for resource in htmlURLS:
            try:
                #metodo che dato il set di risorse le scarica nel formato "corretto" migliorabile
                result=funcs.resourcesDown(resource,counter)
            except:
                print("exception")
            counter=counter+1
        print("lunghezza. ",len(htmlURLS))
    except Exception as e:
        print(e.__cause__)
    finally:
        print("end")
        #chiusura driver
        driver.close()
        #fine misurazione tempi e stampa per eventuali test
        print("--- %s seconds ---" % (time.time() - start_time))    
        
