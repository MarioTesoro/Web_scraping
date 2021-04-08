class Resource:
  def __init__(self):
    self.url = None
    self.format = None
    self.filename = None
    self.newFilename = None
    self.alt = None
    self.text = None
    self.status = None

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
        return url
    
    def getFileName(self):
        return filename

    def getFormat (self):
        return format

    def getAlt(self):
        return alt
    
    def getNewFilename(self):
        return newFilename

    def getText(self):
        return text

    def getStatus(self):
        return status

    def toCSV(self):
        if self.url!=None & self.format != None & self.filename != None & self.newFilename != None & self.alt != None & self.text != None & self.status != None:
            print("csv")
        else:
            return False


