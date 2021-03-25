import web_scraping
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time
from webdriver_manager.chrome import ChromeDriverManager

#url = input("Type website url: ")
def getDownloadPath():
    download_path = os.path.dirname(os.path.realpath(__file__))
    return download_path

print("Web scraping analyisis")
urls=['https://brave-goldberg-4b2f82.netlify.app']
downlaod_path= getDownloadPath()
driver = webdriver.Chrome(ChromeDriverManager().install())
for url in urls: 
    driver.get(url)
    element= driver.find_element_by_tag_name('body')
    element.send_keys(Keys.END)
    web_scraping.sourceCodeDownloader(url,downlaod_path)
    #web_scraping.imagedown(url)
        

driver.close()