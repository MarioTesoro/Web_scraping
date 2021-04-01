import os
import urllib.parse
from urllib.parse import urlparse,urlsplit,parse_qs
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def parseUrl(url):
    parsed_url = urllib.parse.urlparse(url)
    print(parsed_url.netloc)
    return parsed_url.netloc

url= 'https://www.amazon.com/s?k=welder&page=3&qid=1617181389&ref=sr_pg_3'

"""urlPath= urlsplit(url)
values = parse_qs(urlsplit(url).query)
print(values)
#anche questo per ricomporre l'url
o = urlparse(url)
query = parse_qs(o.query)
# extract the URL without query parameters
urlz = o._replace(query=None).geturl()
print(urlz)

if (urlz in url):
    print(True)
    """

def pagination(driver,urlPath):
    try:
        """
        prova = driver.find_elements_by_partial_link_text("Next")
        for pv in prova:
            if pv:
                pv.click()"""
    except:
        print("here")
    netloc = urlPath.netloc
    scheme =urlPath.scheme
    path = urlPath.path
    par = urlPath.params
    link =scheme+"://"+netloc+path
    print(link)
    linkLen= len(link)
    elems = driver.find_elements_by_xpath(('//a[contains(@href, "%s")]' % path) or ('//a[contains(text(), "%s")]' % "Next") or ('//a[contains(text(), "%s")]' %"Show more"))
    print("lens" + str(len(elems)))
    for elem in elems:
        href = elem.get_attribute("href")
        print(href)
        if href[:linkLen] == link:
            try:
                y = elem.click()
                return 
            except:
                print(y)
                break
    return driver.page_source

def finder(page,url):
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
    i=0
    images = soup.find_all('img',alt=True,recursive=True)
    for image in images:
        link=None
        alt=''
        dataSrc =image.get('data-src')
        if dataSrc!=None:
            link= dataSrc
            alt = image.get('alt','')
        elif 'src' in image:
            link = image['src']
            alt = image.get('alt','')
        else:
            print('new tag')
        #formatting url
        print('link:',link)
        print('alt',alt)
        link = checkURLformat(url,link)
        htmlPath.add(link)
        alts.add(alt)

    #funzioni
    aTags = soup.findAll(href=True)
    print(aTags)
    for aTag in aTags:
        href = aTag['href']
        print("href: "+ str(href))
        href = checkURLformat(url,href)
        htmlPath.add(href)

    #print(htmlPath)
    return htmlPath,alts

def checkURLformat(url,link):
    if link!=None:
        if (link[:5] == "http:" ) or (link[:6] =="https:"):
            return link
        elif(link[:1]== "/"):
            return url+link
        else:
            return link

    
