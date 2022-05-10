from scraper import start_scrape
from text_predictor import *
import os
from ImageAnalyzer import PicRecognizer,importPathsFromCSV,topNImages,appendToReport,writeLastRowAnalyzed


def readOkfILE(filename):
    try:
        with open(filename, "r",encoding="utf-8") as f:
            line=f.readline()
        f.close()
        return str(line)
    # Do something with the file
    except IOError:
        print("File not accessible")
        return False


def scrape_and_analyze():
    #tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
    safetytime = 60
    #tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
    loadingtime = 7
    #variabile che indica un valore massimo per il deep scraping di pagine annidate
    maxNumberOfPages=100000
    #grado di dettaglio del report
    detail=False
    #file su cui è scritto un valore che indica la chiusura della GUI
    status_filename='importStatus.txt'
    #file .csv per l'AI
    csv_filename='BigFile.csv'
    #file in cui viene scritta l'ultima riga di cui si è effettuata l'analisi
    txtFilename='lastRow.txt'
    #serve a limitare le chiamate
    callLimit=300
    #quanto deve essere accurata la deduzione del contenuto pornografico
    porn_confidence=0.8
    #quanto deve essere accurata la deduzione dell'età del volto individuato
    age_confidence=0.8
    
    import_status=readOkfILE(status_filename)
    if os.path.exists(status_filename):
        os.remove(status_filename)
    if  import_status == "done":
        #scraping
        start_scrape(safetytime,loadingtime,detail,maxNumberOfPages)
        #image detection
        pathList=importPathsFromCSV(csv_filename,txtFilename)
        numberOfCall,pedoImages,websites=PicRecognizer(pathList,callLimit,txtFilename,porn_confidence,age_confidence)
        #print(pedoImages)
        if numberOfCall!=True:
            lastObjectPath=pathList[numberOfCall-1]
            line=lastObjectPath['line']
            status=writeLastRowAnalyzed(txtFilename,line)#lastRow
        else:
            if os.path.exists(txtFilename):
                os.remove(txtFilename)
        print("pedoimages",pedoImages)
        print("--------------------------------------------------------------")
        topN=topNImages(pedoImages,5,websites)
        appendToReport(topN)
        
    print("Fine scansione")

def analyzedText():
     #text detection
    ai_text_model = loadModel('outputs_training/')
    analyzeFile("BigFile.csv", ai_text_model)
    

