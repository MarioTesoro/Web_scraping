import pywebcopy
import requests
from utils.Utils import *
import os
from model.resource import *
class Downloader:
    #metodo che in base ai formati noti dei file scarica il loro contenuto inoltre popola dei dati inerenti ai file gli oggetti 
    #di tipo Resource e li restituisce al set
    def resourcesDown(self,resource : Resource,counter,srcFolder,hrefFolder):
        url =resource.getUrl()
        print(url)
        #nel file csv scrivo tutto
        filename = os.path.basename(url)
        resource.setFileName(filename)
        format = None
        if resource.tagName == 'a':
           folder= hrefFolder
        else:
            folder =srcFolder

        if(url.endswith("/") or url.endswith(".js") or url.endswith(".css") or url.endswith("html") or url.endswith("htm")):
            resource.setFormat(format)
        elif(url!=None):
            im = requests.get(url)
            if(im.ok):
                resource.setStatus(str(im.status_code))
                print("Filename: "+filename)
                #controllare
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
                        with open(folder + stringedCounter + format, 'wb') as f:
                                print('Writing: ', stringedCounter + format)
                                f.write(im.content) 
                                f.close   
                        resource.setNewFilename(stringedCounter + format)
                    except:
                        print(stringedCounter)
                            #scrivere un file di log
                        pass
            else:
                resource.setStatus(str(im.status_code))
                
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

    def mkDirForUrl(self,url,c):
        folder=Utils().parseUrl(url)
        cwd = os.getcwd()
        #controllo che le cartelle abbiano il suddetto path
        srcFolder =  cwd +os.path.sep+folder +str(c)+ os.path.sep+"src"+os.path.sep
        hrefFolder = cwd +os.path.sep+folder +str(c)+ os.path.sep+"href"+os.path.sep
        print(srcFolder)
        print(hrefFolder)
        try:
            if not os.path.exists(srcFolder) and  not os.path.exists(hrefFolder):
                os.mkdir(os.path.join(os.getcwd(), folder+str(c)))
                os.mkdir(srcFolder)
                os.mkdir(hrefFolder)
            else:
                print("not ok")
        except:
            pass
        return srcFolder,hrefFolder
        #os.chdir(os.path.join(os.getcwd(), folder))
