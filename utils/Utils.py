import urllib.parse
import os
import csv
class Utils:
    #metodo che legge per ogni file .csv nella directory impostata il relativo contenuto e restituisce un array di url e id(da incapsulare)
    def getCSVfromdir(self,directoryPath):
        numberOfRows = 1
        #directory = r'C:\Users\admin'
        for filename in os.listdir(directoryPath):
            if filename.endswith(".csv"):
                with open(filename ,'r') as r_out_f:
                    reader = csv.reader(r_out_f, delimiter=';')
                    #qui viene controllata la prima riga, ovvero l'header del file
                    row1 = next(reader)
                    if len(row1)== 2 and row1[0] =='ID' and row1[1] =='URL':
                        #qui estratti gli Url già presenti nel file
                        #e il numero di righe presenti
                        listofExistingsite = []
                        listofID =[]
                        for rows in reader:
                            listofID.append(rows[0])
                            listofExistingsite.append(rows[1])
                            numberOfRows += 1
                        r_out_f.close()
            else:
                continue
        return

    #metodo che verifica il foromato degli url concatenando lo schema e il nome dell'host in maniera standard
    def checkURLformat(self,url,link):
        if link!=None:
            if (link[:5] == "http:" ) or (link[:6] =="https:"):
                return link
            elif (link[:2]== "//"):
                link = url+link[:1]
            elif(link[:1]== "/"):
                link= url+link
            elif(link[:3] == "../"):
                link = url+"/"+link[3:]
            elif(link[:2] =="./"):
                link =url+"/"+link[2:]
            else:
                print("else",link)
            print(link)
            return link
    
    def parseUrl(self,url):
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc
    
    def getDownloadPath(self):
        download_path = os.getcwd()
        return download_path
