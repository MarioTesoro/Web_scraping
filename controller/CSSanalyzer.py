import requests
from bs4 import BeautifulSoup
import re
from model.webpageInfo import *
from model.resource import *
from utils.Utils import *

class CSSanalyzer:
    webpageInfo = WebpageInfo()    
    """
    # metodo che ricerca i fogli css leggendo l'head della struttura html della pagina e restituisce un set di url ricavati
    def findCssSheets(self,url,page):
            if(url.endswith("/")):
                url=url[:-1]
            soup = BeautifulSoup(page, 'html.parser')
            cssPath = set()
            links = soup.find_all('link')
            sheets = []
            for link in links:
                print(link)
                href = link.attrs.get("href")
                if('.css' in href):  
                    if (href[:5] == "http:" ) or (href[:6] =="https:"):
                        cssPath.add(href)
                    elif (href[:2]== "//"):
                        href = url+href[:1]
                        cssPath.add(href)
                    elif(href[:1]== "/"):
                        href= url+href
                        cssPath.add(href)
                        #print(cssPath)
            return cssPath
        """

    #metodo che dati in input gli url dei fogli di stile trovati effettua uno scraping dei tag richiesti come ad esempio url()
    #restituisce un set di url trovati nei fogli
    def cssParser(self,sheetURL,mainURL) ->set():
            if(mainURL.endswith("/")):
                mainURL=mainURL[:-1]

            r = requests.get(sheetURL)
            css = r.content
            urls = []
            cssURLS = set()
            urls = re.findall('url\(([^)]+)\)',str(css))
            for res in urls:
                r = Resource()
                r.setAlt('fromCss')
                #sostituire con checkURLformat()
                if (res[:5] == "http:" ) or (res[:6] == "https:"):
                    r.setUrl(res)
                elif(res[:3] == "../"):
                    r.setUrl(mainURL+"/"+res[3:])
                elif(res[:2] =="./"):
                    r.setUrl(mainURL+"/"+res[2:])
                elif (res[:2]== "//"):
                    r.setUrl(mainURL+res[:1])
                elif(res[:1]== "/"):
                    r.setUrl(mainURL+res)
                self.webpageInfo.setResource(r)
            return self.webpageInfo.getResources()

            