import requests
from bs4 import BeautifulSoup
import re


class CSSanalyzer:
    def __init__(self):
        super().__init__()    

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


    def cssParser(self,sheetURL,mainURL):
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
                if (res[:5] == "http:" ) or (res[:6] == "https:"):
                    cssURLS.add(res)
                elif(res[:3] == "../"):
                    cssURLS.add(mainURL+"/"+res[3:])
                elif(res[:2] =="./"):
                    cssURLS.add(mainURL+"/"+res[2:])
                elif (res[:2]== "//"):
                    cssURLS.add(mainURL+res[:1])
                elif(res[:1]== "/"):
                    cssURLS.add(mainURL+res)
            return cssURLS

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
        

            