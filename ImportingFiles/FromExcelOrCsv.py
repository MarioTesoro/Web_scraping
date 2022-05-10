import pandas as pd                             #libreria per convertire file da excel a csv
import csv                                      #libreria per gestire i CSV   
from EmailManagement.Inbox import find          #metodo find importato per trovare URl 
                                                #all'interno di stringhe

#metodo utilizzato per effettuare la conversione da file excel a csv
def moveFromExcel(filepath):
    #viene utilizzato pandas per effettuare una conversione del file
    read_file = pd.read_excel (filepath, sheet_name='Foglio1')
    dataframe = pd.DataFrame(read_file)
    #importato in una specifica directory
    target_path = 'Temporary.csv'
    dataframe.to_csv (target_path, index = None, header=True)
    #e poi vengono estratti i dati dal nuovo file csv e importati nel file 'Master'
    urls = moveFromCsv(target_path,True)
    return urls

#metodo utilizzato per prendere URL da file CSV
def moveFromCsv(filepath,fromExcel = False):
    urls = []
    #il file sorgente viene aperto in lettura
    file = open (filepath, 'r') 
    #se proviene da un file excel, tramite conversione pandas
    #il divisore delle colonne sarà messo di default come ','
    if fromExcel:
      reader = csv.reader(file, delimiter=',')
    #altrimenti se gestito da noi, sarà sempre come ';'
    else: 
      reader = csv.reader(file, delimiter=';')
    #viene saltato l'header del file, quindi  la prima riga
    next(reader)
    #vengon prelevati gli URL dalla seconda colonna, ovvero quella relativa agli URL
    for row in reader:
        urls.extend(find(row[1]))
        #e viene controllato che non ci siano url duplicati, in tal caso, ne viene lasciato solo uno
        urls = list(dict.fromkeys(urls))
    file.close()
    return urls
