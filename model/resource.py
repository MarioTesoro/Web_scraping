class Resource:
    url = None
    format = None
    filename = None
    newFilename = None
    alt = None
    text = None
    status = None

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
    def getUrl(self):
        return self.url
    
    def getFileName(self):
        return self.filename

    def getFormat (self):
        return self.format

    def getAlt(self):
        return self.alt
    
    def getNewFilename(self):
        return self.newFilename

    def getText(self):
        return self.text

    def getStatus(self):
        return self.status
        
    def printAll(self):
        print("url"+self.url) 
        print("format " +self.format)
        print("filename " + self.filename)
        print("newFilename " + self.newFilename)
        print("alt " + self.alt)
        print("text " +self.text)
        print("status " +  self.status)

   


