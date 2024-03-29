import time
import os
from utils.Utils import *
from bs4 import BeautifulSoup
from Model.resource import *
from Model.webpageInfo import *
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
            
            if abs(new_height - last_height)<=5:#fixing?
                # If heights are the same it will exit the function
                return
            last_height = new_height
    #metodo che ricerca src datasrc href e alt nei tag img video iframe e alt aggiungendoli al set di risorse comune tra analisi css e html
    def resourceFinder(self,driver,url,translatedNext,translatedPrevious,translatedMore):
            print("Beginning html parsing")
            self.webpageInfo.clearResources()
            page = driver.page_source
            #parse url
            parsedURL = urlparse(url)
            netloc = parsedURL.netloc
            scheme =parsedURL.scheme
            
            #discutere con o senza path
            #shorterLink =scheme+"://"+netloc+path
            shorterLink =scheme+"://"+netloc
            linkLen= len(shorterLink)
            nextHrefs =[]
            previousHrefs=[]
            moreHrefs =[]
            acceptButt = None 
            cssLinks=set()
            soup = BeautifulSoup(page, 'html.parser')
            i=0
            #importante per evitare che venga concatenato male
            if(url.endswith("/")):
                url=url[:-1]
            resources = soup.find_all(recursive=True)
            for resource in resources:
                tagName = resource.name
                link = None
                hrefLink = None
                alt=None
                
                dataSrc =resource.get('data-src')
                src =resource.has_attr('src')
                href = resource.has_attr('href')
                text = resource.get_text()
                #AcceptButt
                if "Accetta" in text or "Accept" in text:
                    acceptButt = self.xpath_soup(resource)
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
                    hrefLink = resource.get('href')
                    print("href:",hrefLink )
                    alt = resource.get('alt','')
                    #formatting url
                    hrefLink = Utils().checkURLformat(url,hrefLink)
                    if(tagName== "link" and hrefLink.endswith(".css")):
                        #un link css viene aggiunto per il parser css ma è inutile fare di esso una risorsa 
                        cssLinks.add(hrefLink)
                        continue
                    if text!=False and text!=None and len(text):
                        #prendo i primi 15 caratteri anzichè tutto il testo per migliorare i tempi
                        lowerText= text.lower()
                        if (hrefLink[:linkLen] == shorterLink):
                            if ("prev" in lowerText) or (translatedPrevious in lowerText) or ("precedente" in lowerText):
                                prevXPATH = self.xpath_soup(resource)
                                previousHrefs.append(prevXPATH)
                            elif ("next" in lowerText) or  (translatedNext in lowerText) or ("prossimo" in lowerText):
                                nextXPATH=self.xpath_soup(resource)
                                nextHrefs.append(nextXPATH)
                            
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
                r.setHref(hrefLink)
                #r.printAll()
                self.webpageInfo.setResource(r)

            return self.webpageInfo.getResources(),previousHrefs,nextHrefs,moreHrefs,cssLinks,acceptButt

    
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
    def findGoNext(self,driver,nextHrefs):
        if len(nextHrefs)>0:
            for elem in reversed(nextHrefs):
                try:
                    self.click(driver,5,elem)
                    return elem
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
        else:
            return "NoElements"
        return False
        
    def findGoBack(self,driver,previousHrefs):
        if len(previousHrefs)>0:
            for elem in reversed(previousHrefs): 
                try:
                    self.click(driver,5,elem)
                    return elem
                except WebDriverException:
                    print( "Elemento non cliccabile")
                    pass
        else:
            return "NoElements"
        return False

    def click(self,driver,delay,xpath):
        selen_elem =driver.find_element_by_xpath(xpath)
        driver.execute_script("arguments[0].scrollIntoView();", selen_elem)
        time.sleep(1)
        selen_elem.click()
        print("click: ")
        time.sleep(4)
        return driver.current_url

        
    """def goBack(self,driver,previousHrefs):
        xpath = self.findGoBack(driver,previousHrefs)
        while xpath!=False:
            if xpath == "NoElements":
                print("NoElements")
                break
            try:
                self.click(driver,5,xpath)
            except WebDriverException:
                print( "Elemento non più cliccabile,cercando di nuovo1")
                return "research"
                """
                    
    """def goNext(self,driver,nextHrefs):
        #funzione che  va avanti il piu possibile 
        xpath = self.findGoNext(driver,nextHrefs)
        while xpath!=False:
            if xpath == "NoElements":
                print("NoElements")
                break
            try:
                self.click(driver,5,xpath)
            except WebDriverException:
                print( "Elemento non più cliccabile,cercando di nuovo")
                break"""
    def showMore(self,moreHrefs):
        return

                