import requests
from bs4 import BeautifulSoup
import re
from model.webpageInfo import *
from model.resource import *

class CSSanalyzer:
    webpageInfo = WebpageInfo()    

    def findCssSheets(self,url,page):
            if(url.endswith("/")):
                url=url[:-1]
                print("urlll",url)
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


    def cssParser(self,sheetURL,mainURL) ->set():
            if(mainURL.endswith("/")):
                mainURL=mainURL[:-1]
                print("urlll",mainURL)
            r = requests.get(sheetURL)
            css = r.content
            urls = []
            cssURLS = set()
            #stringedSheet = str(css)
            urls = re.findall('url\(([^)]+)\)',str(css))
            for res in urls:
                r = Resource()
                r.setAlt('fromCss')
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
        

            