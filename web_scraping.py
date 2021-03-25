import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.parse import ParseResult
import pywebcopy
import pathlib
import cssutils 
#from selenium import webdriver
#from selenium.webdriver.common.keys import Keys

def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    print(parsed_url.netloc)
    return parsed_url.netloc

def imagedown(url):
    folder=parseUrl(url)
    print("Beginning imagedown")
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


#imagedown(url)




def sourceCodeDownloader(url,download_path): 
    kwargs = {'bypass_robots': True}
    #settare bene
    try:
        pywebcopy.config['ALLOWED_FILE_EXT'] = ['.html', '.css','.js']
        pywebcopy.save_webpage(url, download_path , **kwargs)
    except:
        return False
    return True


def cssParseURL(url,download_path):
    folderName = parseUrl(url)
    parser = cssutils.CSSParser()
    css_path=download_path+"/"+folderName+"/"+folderName+"/"+"css"
    for filename in os.listdir(css_path):
        css_sheet_path=css_path +"/"+ filename
        print(css_sheet_path)
        sheet = parser.parseFile(css_sheet_path,'ascii')
        print(sheet.cssText)
