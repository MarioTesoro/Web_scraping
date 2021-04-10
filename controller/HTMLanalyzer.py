import time
import os
from utils.Utils import *
from bs4 import BeautifulSoup
from model.resource import *
from model.webpageInfo import *
class HTMLanalyzer:
    
    webpageInfo = WebpageInfo() 

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
                dataSrc =image.get('data-src')
                src =image.has_attr('src')
                gotsrc=image.get('src')
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
                self.webpageInfo.setResource(r)
                print('link:',r.getUrl)
                print('alt',r.getAlt)

            #funzioni
            aTags = soup.findAll(href=True)
            print(aTags)

            for aTag in aTags:
                href = aTag['href']
                print("href: "+ str(href))
                href = Utils().checkURLformat(url,href)
                r = Resource()
                r.setAlt('aTag')
                r.setUrl(link)
                self.webpageInfo.setResource(r)
            
            videoTags = soup.findAll('video')
            print(videoTags)
            for videoTag in videoTags:
                vdSrc=videoTag.get('src')
                if vdSrc:
                    videoAlt= videoTag.get('alt','')
                elif vdSrc==None:
                    continue
                else:
                    print('new video tag')
                #per i video?
                vdSrc = Utils().checkURLformat(url,vdSrc)
                print("video: ",vdSrc)
                r = Resource()
                r.setAlt(vdSrc)
                r.setUrl(videoAlt)
                self.webpageInfo.setResource(r)

            return self.webpageInfo.getResources()