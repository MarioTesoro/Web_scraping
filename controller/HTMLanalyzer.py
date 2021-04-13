import time
import os
from utils.Utils import *
from bs4 import BeautifulSoup
from model.resource import *
from model.webpageInfo import *

class HTMLanalyzer:
    
    webpageInfo = WebpageInfo() 

    #metodo che effettua uno scroll della pagina impostando un tempo di delay per il caricamento delle risorse e un tempo massimo di scroll
    def scroll(self,driver,loadingtime,safetytime):
        scroll_pause_time = loadingtime
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
    #metodo che ricerca src datasrc href e alt nei tag img video iframe e alt aggiungendoli al set di risorse comune tra analisi css e html
    def resourceFinder(self,page,url):
            print("Beginning html parsing")
            htmlPath = set()
            folder=Utils().parseUrl(url)
            try:
                os.mkdir(os.path.join(os.getcwd(), folder))
                os.mkdir(os.path.join(os.getcwd(), folder+ os.path.sep+"src"))
                os.mkdir(os.path.join(os.getcwd(), folder +os.path.sep+"href"))
            except:
                pass
            os.chdir(os.path.join(os.getcwd(), folder))
            soup = BeautifulSoup(page, 'html.parser')
            i=0
            if(url.endswith("/")):
                url=url[:-1]
            resources = soup.find_all(recursive=True)
            for resource in resources:
                tagName = resource.name
                link = None
                href = 'noHref'
                alt='noAlt'
                text='noText'
                dataSrc =resource.get('data-src')
                src =resource.has_attr('src')
                href = resource.has_attr('href')
                
                text = resource.get_text()
                if dataSrc!=None:
                    link= dataSrc
                    alt = resource.get('alt','')
                    
                elif src:
                    link = resource['src']
                    alt = resource.get('alt','')
                    #input ('inserisci qualcosa')
                elif href: 
                    link = resource.get('href')
                    print("href:",link )
                    alt = resource.get('alt','')
                
                #formatting url
                link = Utils().checkURLformat(url,link)
    
                r = Resource()
                r.setTagName(str(tagName))
                r.setAlt(alt)
                r.setUrl(link)
                r.setText(text.strip())
                r.printAll()
                self.webpageInfo.setResource(r)

            return self.webpageInfo.getResources()
