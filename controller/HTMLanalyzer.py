import time
import os
from utils.Utils import *
from bs4 import BeautifulSoup
from model.resource import *
from model.webpageInfo import *
from urllib.parse import urlparse
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
            input("qui")
            if abs(new_height - last_height)<=5:#fixing?
                # If heights are the same it will exit the function
                return
            last_height = new_height
    #metodo che ricerca src datasrc href e alt nei tag img video iframe e alt aggiungendoli al set di risorse comune tra analisi css e html
    def resourceFinder(self,driver,url,translatedNext,translatedPrevious,translatedMore):
            print("Beginning html parsing")
            page = driver.page_source
            #parse url
            parsedURL = urlparse(url)
            netloc = parsedURL.netloc
            scheme =parsedURL.scheme
            path = parsedURL.path
            par = parsedURL.params
            #discutere con o senza path
            #shorterLink =scheme+"://"+netloc+path
            shorterLink =scheme+"://"+netloc
            linkLen= len(shorterLink)
            nextHrefs =[]
            previousHrefs=[]
            moreHrefs =[]
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
                    #formatting url
                    link = Utils().checkURLformat(url,link)
                elif src:
                    link = resource['src']
                    alt = resource.get('alt','')
                    #input ('inserisci qualcosa')
                    #formatting url
                    link = Utils().checkURLformat(url,link)
                elif href:
                    link = resource.get('href')
                    print("href:",link )
                    alt = resource.get('alt','')
                    #formatting url
                    link = Utils().checkURLformat(url,link)
                    if text!=False and text!=None and len(text):
                        lowerText= text.lower()
                        if (link[:linkLen] == shorterLink and "prev" in lowerText) or  (link[:linkLen] == shorterLink and translatedPrevious in lowerText):
                            prevXPATH = self.xpath_soup(resource)
                           
                            previousHrefs.append(prevXPATH)
                            print("lowertext ",lowerText)
                            print('link[] ',link[:linkLen])
                            print('shorterLink ',shorterLink)
                           
                        elif (link[:linkLen] == shorterLink and "next" in lowerText) or  (link[:linkLen] == shorterLink and translatedNext in lowerText):
                            nextXPATH=self.xpath_soup(resource)
                            
                            nextHrefs.append(nextXPATH)
                            print("lowertext ",lowerText)
                            print('link[] ',link[:linkLen])
                            print('shorterLink ',shorterLink)
                            
                        """
                        elif ("more" in lowerText) or  (translatedMore in lowerText):
                            moreXPATH=self.xpath_soup(resource)
                            selenium_element = driver.find_element_by_xpath(moreXPATH)
                            moreHrefs.append(selenium_element)
                            print("lowertext ",lowerText)
                            print('link[] ',link[:linkLen])
                            print('shorterLink ',shorterLink)
                            input("insert")
                        """
                
                    
                
    
                r = Resource()
                r.setTagName(str(tagName))
                r.setAlt(alt)
                r.setUrl(link)
                r.setText(text.strip())
                r.printAll()
                self.webpageInfo.setResource(r)

            return self.webpageInfo.getResources(),previousHrefs,nextHrefs,moreHrefs

    
    def xpath_soup(self,element):
        # type: (typing.Union[bs4.element.Tag, bs4.element.NavigableString]) -> str
        components = []
        child = element if element.name else element.parent
        for parent in child.parents:  # type: bs4.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if 1 == len(siblings) else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, 1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)
    
    #pagination component
    def goNext(self,nextHrefs,found):
        if len(nextHrefs)>0:
            for elem in nextHrefs:
                try:
                    elem.click()
                    print("click")
                    return elem
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
        return False
    
        
    def goBack(self,driver,previousHrefs):
        if len(previousHrefs)>0:
            for elem in previousHrefs:
                selenium_element = driver.find_element_by_xpath(elem)
                driver.execute_script("arguments[0].scrollIntoView();", selenium_element)
                try:
                    print("click")
                    time.sleep(5)
                    selenium_element.click()
                    return elem
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
        else:
            return "NoElements"
        return False
    
    def showMore(self,moreHrefs):
        return

