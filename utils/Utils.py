import urllib.parse
import os

class Utils:


    def checkURLformat(self,url,link):
        if link!=None:
            if (link[:5] == "http:" ) or (link[:6] =="https:"):
                return link
            elif (link[:2]== "//"):
                link = url+link[:1]
            elif(link[:1]== "/"):
                link= url+link
            elif(link[:3] == "../"):
                link = url+"/"+link[3:]
            elif(link[:2] =="./"):
                link =url+"/"+link[2:]
            else:
                print("else",link)
            print(link)
            return link
    
    def parseUrl(self,url):
        parsed_url = urllib.parse.urlparse(url)
        print(parsed_url.netloc)
        return parsed_url.netloc
    
    def getDownloadPath(self):
        download_path = os.getcwd()
        return download_path
