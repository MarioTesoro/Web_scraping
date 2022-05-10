import csv
import requests
import os
from operator import itemgetter
from Model.PedoImage import PedoImage
from Model.statistics import Statistics
from decouple import config 

def writeLastRowAnalyzed(filename,line):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w",encoding="utf-8") as f:
            f.write(str(line)) 
        f.close()
        return True
    # Do something with the file
    except IOError:
        print("File not accessible")
        return False
        
def readLastRowAnalyzed(filename)->int:
    try:
        with open(filename, "r",encoding="utf-8") as f:
            lastRow=f.readline()
        f.close()
        return int(lastRow)
    # Do something with the file
    except IOError:
        print("File not accessible")
        return False
def importPathsFromCSV(filename,txtfile)->list:
    paths=list()
    value=readLastRowAnalyzed(txtfile)
    if value==False:
        value=1
    try:
        with open(filename,encoding="utf-8") as f:
            # pass the file object to reader() to get the reader object
            csv_reader = csv.reader(f)
            head= next(csv_reader)
            header = list(head)
            print(len(header))
            if len(header)==5 and header[0]=='VALUE' and header[1]=='HOSTNAME' and header[2]=='TEXT' and header[3]=='PATH' and header[4]=='ANALYZED':
                # Iterate over each row in the csv using reader object
                #parte da due perchè l'header di bigCSV è già la prima riga
                counter=2
                for row in csv_reader:
                    if counter<=value:
                        pass
                    else:
                        if row[3] != '':
                            temp_path = row[3]
                            if not temp_path.endswith('.svg'):
                                object_path = {
                                    "hostname":row[1],
                                    "local_path": row[3],
                                    "line":counter,
                                    }
                                paths.append(object_path)
                    counter=counter+1
                # Do something with the file
            f.close()
        return paths
    except IOError:
        print("File not accessible")
        return paths

def PicRecognizer(pathList,limit,txtFilename,porn_confid,age_confid):
    #set per contare il numero di siti web
    websites=set()
    #conterrà oggetti che si riferiranno alle foto pedopornografiche trovate
    pedoImages=set()
    picpurify_url = 'https://www.picpurify.com/analyse/1.1'
    #contatore che segna quante analisi effettua
    i = 0
    #lista dati sull'età di minori acquisiti in una foto
    for object_path in pathList:
        
        img_data = {'file_image': open(object_path['local_path'], 'rb')}
        print(img_data)
        result_data = requests.get(picpurify_url,files = img_data, data = {"API_KEY": config('PICPURIFYKEY'), "task":"porn_moderation,face_age_detection"})
        result_json = result_data.json()
        #print(result_data.content)
        try:
            porn_moderation = result_json['porn_moderation']
            porn_content = porn_moderation['porn_content']
            porn_confidence = porn_moderation['confidence_score']
            print('porn_content: '+str(porn_content)+'porn_confidence: '+str(porn_confidence))
            face_detection = result_json['face_detection']
            results = face_detection['results']
            #controlla che non sia vuoto ,poichè possono non esserci volti individuati
            if results:
                faces= len(results)
                minors=set()
                for res in results:
                    age_results =res['age_majority']
                    age_decision=age_results['decision']
                    age_confidence=age_results['confidence_score']
                    print("age_decision: "+str(age_decision)+' age_confidence: '+str(age_confidence))
                    #IMPORTANTE mettere minor altrimenti riporta i porno con maggiorenni---------------------------------------------------------------------
                    if(porn_content and age_decision=='minor' and porn_confidence>porn_confid and age_confidence>age_confid):
                        hostname=object_path['hostname']
                        pedo=PedoImage()
                        pedo.set_hostname(hostname)
                        pedo.set_local_path(object_path['local_path'])
                        pedo.set_faces_found(faces)
                        pedo.set_age_confidence(age_confidence)
                        pedo.set_porn_confidence(porn_confidence)
                        #può essere impostata in modo diverso ecco perchè esiste il campo
                        pedo.set_key(age_confidence)
                        pedo.set_counter(1)   
                        pedo.set_id(age_confidence+porn_confidence+faces)
                        print(pedo.get_id())
                        websites.add(hostname)
                        print("hostname",hostname)
                        minors.add(pedo)
                        print("OK")
                    #se è c'è almeno un volto di un minore e l'immagine e considerata come pornografica allora non serve proseguire
                    else:
                        print("Maggiorenne in foto")
                #prendo il volto con più confidency se ce ne sono molteplici 
                numberOfMinors=len(minors)
                if numberOfMinors > 1:
                    mostConfidentImage=max(minors,key = lambda y:y.key)
                    pedoImages.add(mostConfidentImage)
                else:
                    pedoImages.add(pedo)
        except Exception:
            pass
        i+=1
        #limitazione call API
        if limit!=False and i == limit:
            return i,pedoImages,websites
    #se finisce la scansione non c'è bisogno del file che ricorda l'ultima riga
    return True,pedoImages,websites





#numberOfCall=48
def topNImages(pedoImages,N,websites):
    if pedoImages:
        topN=list()
        topImages=sorted(pedoImages,key=lambda x: x.key, reverse=True)#il 5 elemento è la key
        print('topImages: ',topImages)
        lenght= len(topImages)
        #N per sito analizzato
        print("wb",websites)
        for website in websites:
            print("website",website)
            c=1
            for img in topImages:
                pedo_img =PedoImage()
                pedo_img=img
                if website == pedo_img.get_hostname() and c<=N:
                    pedo_img.set_counter(c)
                    topN.append(pedo_img)
                    c=c+1
                elif website == pedo_img.get_hostname() and c>N:
                    break

        return topN
    else:
        return None
    
def appendToReport(topN):
    if topN!=None:
        #chiamare scrittura su word
        for img in topN:
            pedo_img =PedoImage()
            pedo_img=img
            print(pedo_img.get_local_path())
            finalStats=Statistics()
            finalStats.writeImageToDoc(pedo_img,pedo_img.get_counter())
    else:
        print("Nessun volto trovato nelle immagini analizzate")

'''
#file .csv per l'AI
csv_filename='BigFile.csv'
#file in cui viene scritta l'ultima riga di cui si è effettuata l'analisi
txtFilename='lastRow.txt'
#serve a limitare le chiamate
callLimit=2000
#quanto deve essere accurata la deduzione del contenuto pornografico
porn_confidence=0.8
#quanto deve essere accurata la deduzione dell'età del volto individuato
age_confidence=0.8


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
'''