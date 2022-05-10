from model.resource import *
from utils.Utils import *
import csv
import os
from model.statistics import Statistics

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
    def toCSV(self,filename,startTime,docFileName,url,detail):
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
            writer.writerow(['ID','TAG NAME','URL','NOME FILE','NOME ATTUALE','TESTO ALT','HREF','TESTO NEL TAG','FORMATO','STATUS'])
            
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
                writer.writerow([numberOfRows,tagName,r.getUrl(),r.getFileName(),r.getNewFilename(),alt,r.getHref(),r.getText(),r.getFormat(),status])
                numberOfRows+=1
        out_f.close()
        stats =self.writeStatistics(detail,filename,numberOfRows,downloaded,css,a,img,video,others,startTime,docFileName,url)
        return stats
    
    def writeStatistics(self,write,filename,numberOfRows,downloaded,css,a,img,video,others,startTime,docFileName,url)->Statistics:
        cssRatio=css/numberOfRows*100
        htmlRes=numberOfRows- css
        htmlRatio = htmlRes/numberOfRows*100
        aRatio=a/numberOfRows*100
        imgRatio= img/numberOfRows*100
        videoRatio= video/numberOfRows*100
        othersRatio= others/numberOfRows*100
        duration = time.time() - startTime
        #oggetto statistics
        stats = Statistics()
        stats.setRes(numberOfRows)
        stats.setDownloaded(downloaded)
        stats.setCssRes(css)
        stats.setCssRatio(cssRatio)
        stats.setHtmlRes(htmlRes)
        stats.setHtmlRatio(htmlRatio)
        stats.setAres(a)
        stats.setAratio(aRatio)
        stats.setImgRes(img)
        stats.setImgRatio(imgRatio)
        stats.setVideoRes(video)
        stats.setVideoratio(videoRatio)
        stats.setOtherRes(others)
        stats.setOtherRatio(othersRatio)
        stats.setDuration(duration)
        stats.setUrl(url)
        #inizializzazione file doc
        if write:
            stats.writeToDoc(docFileName,True)
        return stats
        
    def appendToDataset(self,netloc):
        if os.path.isfile('BigFile.csv'):
            with open(self.downloadPath+os.path.sep+ str("BigFile")+'.csv' ,'a', newline='',encoding="utf-8") as out_f:
                writer = csv.writer(out_f)
                for resource in self.getResources():
                    alt=resource.getAlt()
                    text = resource.getText()
                    filename = resource.getFileName()
                    if filename!=None and str(filename).strip()!='':
                        writer.writerow([15,netloc,filename])
                    if alt!=None and str(alt).strip()!='':
                        writer.writerow([15,netloc,alt])
                    if text!=None and str(text).strip()!='':
                        writer.writerow([15,netloc,text])
            out_f.close()
            return
        else:
            try:
                with open(self.downloadPath+os.path.sep+ str("BigFile")+'.csv' ,'w', newline='',encoding="utf-8") as out_f:
                    writer = csv.writer(out_f)
                    writer.writerow(['VALUE','HOSTNAME','TEXT'])
                    for resource in self.getResources():
                        alt=resource.getAlt()
                        text =resource.getText()
                        filename =resource.getFileName()
                        if filename!=None and str(filename).strip()!='':
                            writer.writerow([15,netloc,filename])
                        if alt!=None and str(alt).strip()!='':
                            writer.writerow([15,netloc,alt])
                        if text!=None and str(text).strip()!='':
                            writer.writerow([15,netloc,text])
                out_f.close()
            except:
                print("close current file")
                pass
            return
            
           

