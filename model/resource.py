
import time
class Resource:
    tagName =None
    url = None
    format = None
    filename = None
    newFilename = None
    alt = None
    text = None
    status = None
    href =None
    #metodo fondamentale poichè nel set differenzia un oggetto dall'altro,va discussa una politica da adottare in merito
    def __eq__(self, other):
        r= Resource()
        r=other
        """
        if(self.url == r.getUrl() and self.alt == r.getAlt() and self.text==r.getText()):
            return True
        else:
            return False
        """
        
        return self.url == r.getUrl() and self.href == r.getHref() and self.text == r.getText()
    def __hash__(self):
        return hash(self.url)
    #setters
    def setUrl(self,url):
        self.url=url
    
    def setFileName(self,filename):
        self.filename=filename

    def setFormat (self,format):
        self.format=format

    def setAlt(self,alt):
        self.alt=alt
    
    def setNewFilename(self,newFilename):
        self.newFilename=newFilename

    def setText(self,text):
        self.text=text
    def setStatus(self,status):
        self.status = status

    def setTagName(self,tagName):
        self.tagName = tagName
    def setHref(self,href):
        self.href = href
    #getters
    def getUrl(self) -> str:
        return self.url
    
    def getFileName(self) -> str:
        return self.filename

    def getFormat (self) -> str:
        return self.format

    def getAlt(self) -> str:
        return self.alt
    
    def getNewFilename(self) -> str:
        return self.newFilename

    def getText(self) -> str:
        return self.text

    def getStatus(self) -> str:
        return self.status

    def getTagName(self) -> str:
        return self.tagName
    def getHref(self) -> str:
        return self.href
        
    def printAll(self):
        print("url "+str(self.url)) 
        print("format " +str(self.format))
        print("filename " + str(self.filename))
        print("newFilename " + str(self.newFilename))
        print("alt " + str(self.alt))
        print("text " + str(self.text))
        print("status " +  str(self.status))
        print("tagname " +  str(self.tagName))
        print("href " +  str(self.href))

   


