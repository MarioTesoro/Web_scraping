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
            except:
                pass
            os.chdir(os.path.join(os.getcwd(), folder))
            soup = BeautifulSoup(page, 'html.parser')
            i=0
            if(url.endswith("/")):
                url=url[:-1]
                print("urlll",url)
            images = soup.find_all(['img','iframe'],alt=True,recursive=True)
            for image in images:
                link=None
                alt=''
                text=''
                dataSrc =image.get('data-src')
                src =image.has_attr('src')
                gotsrc=image.get('src')
                text = image.get_text()
                if dataSrc!=None:
                    link= dataSrc
                    alt = image.get('alt','')
                if 'src' in image:
                    link = image['src']
                    alt = image.get('alt','')
                
                if src:
                    link = image['src']
                    alt = image.get('alt','')
                  
                if gotsrc!=None:
                    link= image.get('src')
                    alt = image.get('alt','')
                   
                #formatting url
                link = Utils().checkURLformat(url,link)
                r = Resource()
                r.setAlt(alt)
                r.setUrl(link)
                r.setText(text.strip())
                self.webpageInfo.setResource(r)
                print('link: ',r.getUrl())
                print('alt: ',r.getAlt())

            #funzioni
            aTags = soup.findAll(href=True)
            print(aTags)

            for aTag in aTags:
                href = aTag['href']
                text = aTag.get_text()
                href = Utils().checkURLformat(url,href)
                r = Resource()
                r.setAlt('aTag')
                r.setUrl(href)
                r.setText(text.strip())
                self.webpageInfo.setResource(r)
                print("href : "+ str(r.getUrl()))
                print("text :"+str(r.getText()))
            
            videoTags = soup.findAll('video')
            print(videoTags)
            for videoTag in videoTags:
                vdSrc=videoTag.get('src')
                text = videoTag.get_text()
                videoAlt =''
                if vdSrc:
                    videoAlt= videoTag.get('alt','')
                elif vdSrc==None:
                    continue
                else:
                    print('new video tag')
                #per i video?
                vdSrc = Utils().checkURLformat(url,vdSrc)
                r = Resource()
                r.setAlt(videoAlt)
                r.setUrl(vdSrc)
                r.setText(text.strip())
                self.webpageInfo.setResource(r)

            return self.webpageInfo.getResources()
