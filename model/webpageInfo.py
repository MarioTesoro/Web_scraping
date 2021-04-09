from model.resource import *
class WebpageInfo:
    resources= set()
      
    def setResource(self,res):
        self.resources.add(res)

    def extendResources(self,res):
        self.resources.update(res)
    
    def getResources(self):
        return self.resources
    def printResources(self):
        for res in self.resources:
            print(res)

    def toCSV(self):
        if self.url!=None & self.format != None & self.filename != None & self.newFilename != None & self.alt != None & self.text != None & self.status != None:
            print("csv")
        else:
            return False

