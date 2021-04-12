from model.resource import *
from utils.Utils import *
import csv
import os
class WebpageInfo:
    resources = set()
    downloadPath = Utils().getDownloadPath()
    id = None 

    def __init__(self):
        resources=set()

    def setId(self,id):
        self.id=id

    def setResource(self,res : Resource):
        self.resources.add(res)

    def extendResources(self,res):
        self.resources.update(res)
    
    def getResources(self):
        return self.resources

    def getID(self):
        return self.id

    def printResources(self):
        for res in self.resources:
            r =Resource()
            r= res
            r.printAll()
    #metodo che scrive in un file .csv le risorse trovate
    def toCSV(self,filename):
        print("Writing: "+  str(filename)+'.csv')
        numberOfRows = 1
        with open(self.downloadPath+os.path.sep+ str(filename)+'.csv' ,'w', newline='',encoding="utf-8") as out_f:
            writer = csv.writer(out_f, delimiter=';')
            writer.writerow(['ID','URL','NOME FILE','NOME ATTUALE','TESTO ALT','TESTO NEL TAG','FORMATO','STATUS'])
            for res in self.resources:
                r = Resource()
                r = res
                writer.writerow([numberOfRows,r.getUrl(),r.getFileName(),r.getNewFilename(),r.getAlt(),r.getText(),r.getFormat(),r.getStatus()])
                numberOfRows+=1 
            out_f.close()
            #implementare le statistiche
           

