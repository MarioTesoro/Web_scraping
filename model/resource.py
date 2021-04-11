
import time
class Resource:
    url = None
    format = None
    filename = None
    newFilename = None
    alt = None
    text = None
    status = None

    def __eq__(self, other):
        r= Resource()
        r=other
        """
        if(self.url == r.getUrl() and self.alt == r.getAlt() and self.text==r.getText()):
            return True
        else:
            return False
        """
        return self.url == r.getUrl()
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
        
    def printAll(self):
        print("url "+str(self.url)) 
        print("format " +str(self.format))
        print("filename " + str(self.filename))
        print("newFilename " + str(self.newFilename))
        print("alt " + str(self.alt))
        print("text " + str(self.text))
        print("status " +  str(self.status))

   


