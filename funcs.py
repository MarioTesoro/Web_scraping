import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.parse import ParseResult, urljoin
import pywebcopy
import pathlib
import cssutils 
import re

def getDownloadPath():
    download_path = os.path.dirname(os.path.realpath(__file__))
    return download_path

def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    print(parsed_url.netloc)
    return parsed_url.netloc

def HTMLparser(url):
    print("Beginning html parsing")
    htmlPath = set()
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
        print('link: ',link)
        alt = image.get('alt','')
        print('alt',alt)
        if ("http:" in link) or ("https:" in link):
            htmlPath.add(link)
        else:
            htmlPath.add(url+"/"+link)
        i=i+1
    print(htmlPath)
    return htmlPath

def resourcesDown(url):
    filename = os.path.basename(url)
    print(filename)
    """with open(filename, 'wb') as f:
            im = requests.get(url)
            f.write(im.content)
            print('Writing: ', filename)"""

def sourceCodeDownloader(url,download_path): 
    folder=parseUrl(url)
    kwargs = {'bypass_robots': True}
    #settare bene
    try:
        pywebcopy.config['LOAD_JAVASCRIPT']=True
        pywebcopy.config['LOAD_CSS']=True
        pywebcopy.config['OVER_WRITE'] = False
        pywebcopy.config['ALLOWED_FILE_EXT'] = ['.html', '.css','.js']
        pywebcopy.save_webpage(url, download_path , **kwargs)
    except:
        return False
    return True

def cssParseURLS(url,download_path):
    folderName = parseUrl(url)
    parser = cssutils.CSSParser()
    css_path=download_path+"/"+folderName+"/"+folderName+"/"+"css"
    for filename in os.listdir(css_path):
        css_sheet_path=css_path +"/"+ filename
        print(css_sheet_path)
        sheet = parser.parseFile(css_sheet_path,'ascii')
        stringedSheet=str(sheet.cssText)
        urls = re.findall("url\(.+?\)",stringedSheet)
        print(urls)
        print('--------------------------------------------------------------------------------------')
        
def findCssSheets(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    cssPath = set()
    links = soup.find_all('link')
    sheets = []
    for link in links:
        attribute = link.attrs.get("rel")
        if(attribute[0] == 'stylesheet'):
            href = link.attrs.get("href")
            if ("http:" in href) or ("https:" in href):
                cssPath.add(href)
            else:
                cssPath.add(url+"/"+href)
            print(cssPath)
    return cssPath


#cssParseURLS('https://brave-goldberg-4b2f82.netlify.app','C://Users//39320//Desktop//Web_scraping')
