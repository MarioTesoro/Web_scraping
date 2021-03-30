import requests
from bs4 import BeautifulSoup
import os
import urllib.parse
from urllib.parse import ParseResult, urljoin
import pywebcopy
import pathlib
import cssutils
import re
import time

def getDownloadPath():
    download_path = os.path.dirname(os.path.realpath(__file__))
    return download_path

def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    print(parsed_url.netloc)
    return parsed_url.netloc

def HTMLparser(page,url):
    print("Beginning html parsing")
    htmlPath = set()
    alts = set()
    folder=parseUrl(url)
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))
    soup = BeautifulSoup(page, 'html.parser')
    aTag = soup.find_all('a')
    images = soup.find_all('img',alt=True)
    aTags =soup.findAll('a')
    i=0
    for image in images:  
        link = image['src']
        print('link: ',link)
        alt = image.get('alt','')
        print('alt',alt)
        if (link[:5] == "http:" ) or (link[:6] =="https:"):
            htmlPath.add(link)
            alts.add(alt)
        elif(link[:1]== "/"):
            htmlPath.add(url+link)
            alts.add(alt)
        else:
            htmlPath.add(link)
            alts.add(alt)
    #funzioni
    """for aTag in aTags:
        href = aTag['href']
        print("href: "+ str(href))
        if (link[:5] == "http:" ) or (link[:6] =="https:"):
            htmlPath.add(link)
        elif(link[:1]== "/"):
            htmlPath.add(url+link)
        else:
            htmlPath.add(link)"""

    print(htmlPath)
    return htmlPath,alts

def resourcesDown(url,counter):
    im = requests.get(url)
    if(im.ok):
        format = None
        filename = os.path.basename(url)
        print("Filename: "+filename)
        if('jpg' in filename):
            format ='.jpg'
        elif('png' in filename):
            format ='.png'
        elif('jpeg' in filename):
            format ='.jpeg'
        elif('mp4' in filename):
            format= '.mp4'
        elif('svg' in filename):
            format='.svg'
        else:
            format ='.jpg'
            
        if(format !=None):
            stringedCounter = str(counter)
            print(stringedCounter + format)
            """with open(stringedCounter + format, 'wb') as f:
                    f.write(im.content)
                    print('Writing: ', stringedCounter + format)
                    f.close"""
    else:
        print(im.status_code)     
    return True
   


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
"""
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
        """
        
def findCssSheets(url,page):
    soup = BeautifulSoup(page, 'html.parser')
    cssPath = set()
    links = soup.find_all('link')
    sheets = []
    for link in links:
        href = link.attrs.get("href")
        if('.css' in href):  
            if ("http:" in href) or ("https:" in href):
                cssPath.add(href)
            else:
                cssPath.add(url+"/"+href)
            #print(cssPath)
    return cssPath


def scroll(driver , timeout,safetytime):
        scroll_pause_time = timeout
        beginTime= time.time()

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            print(time.time()-beginTime)
            if(time.time()-beginTime >= safetytime):
                return
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            try:
                time.sleep(scroll_pause_time)
            except:
                print("need more timeout")
                return

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            print(new_height, last_height)
            if abs(new_height - last_height)<=5:#fixing?
                # If heights are the same it will exit the function
                return
            last_height = new_height

def cssParser(sheetURL,mainURL):
    r = requests.get(sheetURL)
    css = r.content
    urls = []
    cssURLS = set()
    #stringedSheet = str(css)
    urls = re.findall('url\(([^)]+)\)',str(css))
    for res in urls:
        if (res[:5] == "http:" ) or (res[:6] == "https:"):
            cssURLS.add(res)
        elif(res[:3] == "../"):
            cssURLS.add(mainURL+"/"+res[3:])
        elif(res[:2] =="./"):
            cssURLS.add(mainURL+"/"+res[2:])
    return cssURLS