import pywebcopy
import requests
from utils.Utils import *
import os
from model.resource import *
class Downloader:
    #metodo che in base ai formati noti dei file scarica il loro contenuto inoltre popola dei dati inerenti ai file gli oggetti 
    #di tipo Resource e li restituisce al set
    def resourcesDown(self,resource : Resource,counter):
        url =resource.getUrl()
        print(url)
        #nel file csv scrivo tutto
        filename = os.path.basename(url)
        resource.setFileName(filename)
        format = None
        if(url!=None):
            im = requests.get(url)
            if(im.ok):
                resource.setStatus(im.status_code)
                print("Filename: "+filename)
                if('jpg' in filename):
                    format ='.jpg'
                elif('png' in filename):
                    format ='.png'
                elif('jpeg' in filename):
                    format ='.jpeg'
                elif('mp4' in filename):
                    format= '.mp4'
                elif('svg' in filename):
                    format='.svg'
                elif('gif' in filename):
                    format='.gif'
                elif('woff' in filename):
                    format='.woff'
                else:
                    #stampa l'url per capire l'estensione e migliorare
                    print(url)
                    format ='.jpg' #.jpg
                        
                if(format !=None):
                    resource.setFormat(format)
                    stringedCounter = str(counter)
                    print(stringedCounter + format)
                    try:
                        with open(stringedCounter + format, 'wb') as f:
                                print('Writing: ', stringedCounter + format)
                                f.write(im.content) 
                                f.close   
                        resource.setNewFilename(stringedCounter + format)
                    except:
                        print(stringedCounter)
                            #scrivere un file di log
                        pass
            else:
                resource.setStatus(im.status_code)
                
                print("URL:" +str(im.status_code),url)   
        else:
            resource.setFormat(format)
            #not donwoloaded  
        return counter
        

    #metodo per il download del source code, da discutere
    def sourceCodeDownloader(self,url,download_path): 
        folder=Utils().parseUrl(url)
        kwargs = {'bypass_robots': True}
        #settare bene
        try:
            pywebcopy.config['LOAD_JAVASCRIPT']=True
            pywebcopy.config['LOAD_CSS']=True
            pywebcopy.config['OVER_WRITE'] = False
            pywebcopy.config['ALLOWED_FILE_EXT'] = ['.html', '.css','.js']
            pywebcopy.save_webpage(url, download_path , **kwargs)
        except:
            return False
        return True