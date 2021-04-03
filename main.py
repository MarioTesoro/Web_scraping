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
urls=['https://www.ansa.it/']#'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3' #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor' ''https://it.wikipedia.org/wiki/Pagina_principale''
cssURLS= set()
htmlURLS = set()
alts = set()
downlaod_path = funcs.getDownloadPath()
print(downlaod_path)
driver = webdriver.Chrome(ChromeDriverManager().install())

for url in urls:
    
    urlPath= urlparse(url)
    print(urlPath)
    driver.get(url)
 
    driver.maximize_window()
    print(len(str(driver.page_source)))
    try:
        element = driver.find_element_by_tag_name('body')
        safetytime = 30
        loadingTime= 10
        #result =prova.pagination(driver,urlPath)
        #print(result)
        funcs.scroll(driver,loadingTime,safetytime)
        page = driver.page_source
        #print(len(str(page)))
        # check pagination
        sheets = funcs.findCssSheets(url,page)
        #print(len(sheets))
        if(len(sheets)> 0):
            for sheetURL in sheets:
                print(sheetURL)
                cssURLS.update(funcs.cssParser(sheetURL,url)) 
                print(cssURLS)
                print("---------------------------------------------------------------------\n")
        else:
            print("css not found")
        #downlaod source code
        #funcs.sourceCodeDownloader(url,downlaod_path)
        htmlURLS,alts = prova.finder(page,url)
        #join set() css e html
        htmlURLS.update(cssURLS)
        print(len(htmlURLS))
        print("---------------------------------------------------------------------\n")
        print(alts)
        counter=1
        for resource in htmlURLS:
            try:
                result=funcs.resourcesDown(resource,counter)
            except:
                print("exception")
            counter=counter+1
    except Exception as e:
        print(e.__cause__)
    finally:
        print("ciao")
        #close driver
        driver.close()
        print("--- %s seconds ---" % (time.time() - start_time))    
        
