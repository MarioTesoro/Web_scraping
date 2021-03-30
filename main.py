import funcs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
import requests



#url = input("Type website url: ")
print("Web scraping analyisis")
urls=['https://it.wikipedia.org/wiki/Pagina_principale'] #'https://unsplash.com/' #'https://brave-goldberg-4b2f82.netlify.app' #'https://twitter.com/Twitter?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor'
cssURLS= set()
htmlURLS = set()
alts = set()
downlaod_path = funcs.getDownloadPath()
print(downlaod_path)
driver = webdriver.Chrome(ChromeDriverManager().install())
for url in urls:
    driver.get(url)
    driver.maximize_window()
    print(len(str(driver.page_source)))
    
    try:
        element = driver.find_element_by_tag_name('body')
        safetytime = 30
        loadingTime= 10
        funcs.scroll(driver,loadingTime,safetytime)
        page = driver.page_source
        print(len(str(page)))
        sheets = funcs.findCssSheets(url,page)
        #print(len(sheets))
        if(len(sheets)> 0):
            for sheetURL in sheets:
                print(sheetURL)
                cssURLS.update(funcs.cssParser(sheetURL,url)) 
                print("---------------------------------------------------------------------\n")
        else:
            print("css not found")
        #downlaod source code
        #funcs.sourceCodeDownloader(url,downlaod_path)
        htmlURLS,alts = funcs.HTMLparser(page,url)
        #join set() css e html
        htmlURLS.update(cssURLS)
        print(htmlURLS)
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
        print("time exceeded")
    finally:
        #downlaod files
        #htmlSheets = funcs.HTMLparser(url)
        #close driver
        driver.close()    
