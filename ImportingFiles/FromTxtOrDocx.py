import docx                          #libreria per gestire i file word
from EmailManagement.Inbox import find               #metodo find importato per trovare URl 
                                     #all'interno di stringhe

#metodo utilizzato per prendere URL da file TXT
def takeUrlFromTxt(filepath):
    file =  open(filepath, 'r',encoding="utf-8")
    in_f = file.readlines()
    urls = []
    #per ogni riga del file di testo, vengono prelevati URL se presenti
    for line in in_f:
        urls.extend(find(line))
        #e viene controllato che non ci siano url duplicati, in tal caso, ne viene lasciato solo uno
        urls = list(dict.fromkeys(urls))
    file.close()
    return urls

#metodo utilizzato per trasferire URL da file WORD
def takeUrlFromDocx(filepath):
    urls =  []
    doc = docx.Document(filepath)
    #per ogni paragrafo trovato, vengono prelevati URL se presenti 
    for paragraph in doc.paragraphs:
        urls.extend(find(paragraph.text))
        #e viene controllato che non ci siano url duplicati, in tal caso, ne viene lasciato solo uno
        urls = list(dict.fromkeys(urls))
    return urls

