import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.parse import ParseResult
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url
    )
    print(parsed_url.netloc)
    return parsed_url.netloc

def imagedown(url):
    folder=parseUrl(url)
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img',alt=True)
    i=0
    for image in images:
        name=i
    
        link = image['src']
        alt = image.get('alt','')
        print('link: ',link)
        print('alt',alt)

        """ with open(str(name) + '.jpg', 'wb') as f:
            im = requests.get(link)
            f.write(im.content)
            print('Writing: ', name) """
        i=i+1

#Main
from pywebcopy import save_webpage
import pathlib
#url = input("Type website url: ")
url='https://brave-goldberg-4b2f82.netlify.app'
#imagedown(url)

folderName = parseUrl(url)

download_path = os.path.dirname(os.path.realpath(__file__))
print(download_path)

#kwargs = {'bypass_robots': True}
#save_webpage(url, download_path , **kwargs)

import cssutils 
parser = cssutils.CSSParser()
# optionally
css_path=download_path+"/"+folderName+"/"+folderName+"/"+"css"
for filename in os.listdir(css_path):
    css_sheet_path=css_path +"/"+ filename
    print(css_sheet_path)
    sheet = parser.parseFile(css_sheet_path,'ascii')
    print(sheet.cssText)
