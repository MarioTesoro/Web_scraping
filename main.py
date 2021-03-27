import funcs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

#url = input("Type website url: ")
print("Web scraping analyisis")
urls=['https://brave-goldberg-4b2f82.netlify.app'] #'https://unsplash.com/'
downlaod_path = funcs.getDownloadPath()
print(downlaod_path)
#driver = webdriver.Chrome(ChromeDriverManager().install())
for url in urls: 
    #driver.get(url)
    #element= driver.find_element_by_tag_name('body')
    #element.send_keys(Keys.END)
    #downlaod source code
    #funcs.sourceCodeDownloader(url,downlaod_path)
    #css analisis
    #sheets = funcs.findCssSheets(url)
    #funcs.cssParseURLS(url,downlaod_path)
    #downlaod files
    htmlSheets = funcs.HTMLparser(url)
    #close driver
    #driver.close()    
