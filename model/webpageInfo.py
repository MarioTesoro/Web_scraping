from model.resource import *
from utils.Utils import *
import csv
import os
class WebpageInfo:
    resources = set()
    downloadPath = Utils().getDownloadPath()
    id = None 
    def clearResources(self):
        self.resources.clear()

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
        css=0
        img=0
        video=0
        others=0
        a=0
        downloaded=0
        with open(self.downloadPath+os.path.sep+ str(filename)+'.csv' ,'w', newline='',encoding="utf-8") as out_f:
            writer = csv.writer(out_f, delimiter=';')
            writer.writerow(['ID','TAG NAME','URL','NOME FILE','NOME ATTUALE','TESTO ALT','TESTO NEL TAG','FORMATO','STATUS'])
            
            for res in self.resources:
                r = Resource()
                r = res
                alt =r.getAlt()
                status =r.getStatus()
                tagName=r.getTagName()
                if alt=='fromCss':
                    css+=1
                if status == str(200):
                    downloaded+=1
                if tagName =='a':
                    a+=1
                elif tagName =='img':
                    img+=1
                elif tagName =='video':
                    video+=1
                else:
                    others+=1
                writer.writerow([numberOfRows,tagName,r.getUrl(),r.getFileName(),r.getNewFilename(),alt,r.getText(),r.getFormat(),status])
                numberOfRows+=1 
            out_f.close()
        print("------------------------------Statistiche------------------------")
        print("Risorse ricercate",str(numberOfRows))
        print("Risorse con status 200",str(downloaded))
        print("Risorse trovate dall'analizzatore css:",str(css/numberOfRows)+"%")
        print("Risorse trovate dall'analizzatore html:",str((numberOfRows- css)/numberOfRows)+"%")
        print("Risorse con tag a:",str(a/numberOfRows)+"%")
        print("Risorse con tag img:",str(img/numberOfRows)+"%")
        print("Risorse con tag video:",str(video/numberOfRows)+"%")
        print("Risorse con altri tag:",str(others/numberOfRows)+"%")
            #implementare le statistiche
           

