from matplotlib.pyplot import close
from selenium import webdriver
from controller.HTMLanalyzer import *
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from utils import Utils
import os
from urllib.parse import urlparse
import time
from controller.CSSanalyzer import * 
from controller.Downloader import *
from Model.webpageInfo import *
from Model.statistics import Statistics
from selenium.common.exceptions import WebDriverException




def web_scraper(url,loadingtime,safetytime,detailedReport,maxNumerOfPages,browser):
    print("url",url)
    #inizio fase di analisi
    print("Web scraping analyisis")
    urls=[]
    statsList=[]
    urls.append(url)
    #variabile che rappresenta l'eventuale stato di loop che ha il programma 
    loop =False
    #installazione driver
    driver = None
    #switch browsers
    if browser == "chrome":
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        except:
            print("Chrome is not installed")
    elif browser =="firefox":
        try:
            driver =  webdriver.Firefox() #TODO
        except:
            print("Firefox is not installed")
    else:           
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())
        except:
            driver =  webdriver.Firefox()
        
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
        #driver.maximize_window()#da inserire 
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
        resourceFound,previousHrefs,nextHrefs,moreHrefs,sheets,acceptButt = htmlanalyzer.resourceFinder(driver,url,"avanti","indietro","more")
        print(firstTime)
        #funzione che torna indietro il piu possibile ed effettua in caso una nuova ricerca delle risorse html
        if firstTime:
            print("AcceptButt",acceptButt)
            if acceptButt:
                htmlanalyzer.click(driver,1,acceptButt)
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
            print(url)
            #l'ultimo attributo indica se aggiungere al report le statistiche in detteaglio(True) o meno (False)
            stats = webPageInfo.toCSV(netloc+str(c),start_time,docFileName[2],url,detailedReport)
            statsList.append(stats)
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
        if maxNumerOfPages!=False:
            if c == maxNumerOfPages:
                break
        c=c+1
        webPageInfo.clearResources()
    driver.close()
    return urls,statsList

def write_statistics(url,urlFound,statsList,docFileName):        
    urlFound = set(urlFound)
    totalRes=0
    totalDownload=0
    totalDuration=0
    totalTagImg=0
    totalTagvideo=0
    totalTagOthers=0
    totalTagA=0
    imgRatio= 0
    videoRatio= 0
    othersRatio= 0
    aRatio=0
    htmlRes=0
    cssRes=0
    for stats in statsList:
        totalRes=totalRes+stats.getRes()
        totalDownload=totalDownload+stats.getDownloaded()
        totalDuration=totalDuration+stats.getDuration()
        totalTagA=totalTagA + stats.getAres()
        totalTagImg=totalTagImg+stats.getImgRes()
        totalTagvideo=totalTagvideo+stats.getVideoRes()
        totalTagOthers=totalTagOthers + stats.getOtherRes()
        htmlRes=htmlRes + (stats.getRes()-stats.getCssRes())
        cssRes = cssRes + stats.getCssRes()
    imgRatio= totalTagImg/totalRes*100
    videoRatio= totalTagvideo/totalRes*100
    othersRatio= totalTagOthers/totalRes*100
    aRatio= totalTagA/totalRes*100
    cssRatio=cssRes/totalRes*100
    htmlRatio = htmlRes/totalRes*100
    finalStats=Statistics()
    finalStats.setUrl(url)
    finalStats.setRes(totalRes)
    finalStats.setNumberOfPages(len(urlFound))
    finalStats.setDownloaded(totalDownload)
    finalStats.setDuration(totalDuration)
    finalStats.setImgRes(totalTagImg)
    finalStats.setVideoRes(totalTagvideo)
    finalStats.setOtherRes(totalTagOthers)
    finalStats.setAres(totalTagA)
    finalStats.setHtmlRes(htmlRes)
    finalStats.setCssRes(cssRes)
    #ratio
    finalStats.setImgRatio(imgRatio)
    finalStats.setVideoratio(videoRatio)
    finalStats.setOtherRatio(othersRatio)
    finalStats.setAratio(aRatio)
    finalStats.setCssRatio(cssRatio)
    finalStats.setHtmlRatio(htmlRatio)
    finalStats.writeToDoc(docFileName[2],False)

def start_scraper(urls,output,safetytime,loadingtime,detail,maxNumberOfPages,browser):
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------
    #import urls e id
    #current_dir=os.getcwd()
    #ut = Utils()
    #urls,urlsID = ut.getCSVfromdir(current_dir,"Master.csv")
    # print(urlsID)
    # if not urls or not urlsID:
    #     print("urls are empty or id empty")
    #     os._exit(0)
    if not urls:
        print("urls are empty")
        os._exit(0)
    #urls=['https://www.ansa.it/']
    #https://it.xhamster.com/3 #'https://www.ansa.it/'#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''
    for url in urls:
        print("urls",url)
        docFileName = url.split('/')

        #l'ultimo parametro indica i dettagli del report se False sarà solo un'overview generica altrimenti se True di ogni pagina ci saranno stime più dettagliate
        urlFound,statsList=web_scraper(url,loadingtime,safetytime,False,maxNumberOfPages,browser)
        #totalStats.extend(statsList)
        #totalUrls.extend(urlFound)
        if output:
            write_statistics(url,urlFound,statsList,docFileName)

        
            
            
        
        
        
        
        
