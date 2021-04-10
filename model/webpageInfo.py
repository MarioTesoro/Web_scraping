from model.resource import *
from utils.Utils import *
import csv
import os
class WebpageInfo:
    resources= set()
    downloadPath = Utils().getDownloadPath()
      
    def setResource(self,res : Resource):
        self.resources.add(res)

    def extendResources(self,res):
        self.resources.update(res)
    
    def getResources(self):
        return self.resources
    def printResources(self):
        for res in self.resources:
            print(res)

    def toCSV(self):
        numberOfRows = 1
        with open(self.downloadPath+os.path.sep+ 'csvFile.csv' ,'w', newline='') as out_f:
            writer = csv.writer(out_f, delimiter=';')
            writer.writerow(['ID','URL','NOME FILE','NUOVO NOME','TESTO ASSOCIATO','FORMATO','STATUS'])
            for res in self.resources:
                r = Resource()
                r = res
                writer.writerow([numberOfRows,r.getUrl(),r.getFileName(),r.getNewFilename(),r.getAlt(),r.getFormat(),r.getStatus()])
                numberOfRows+=1 
           

