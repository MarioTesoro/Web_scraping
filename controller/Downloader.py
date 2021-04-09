import pywebcopy
import requests
from utils.Utils import *
import os
class Downloader:
    
    def resourcesDown(self,url,counter):
        im = requests.get(url)
        if(im.ok):
            format = None
            filename = os.path.basename(url)
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
            else:
                format ='jpg' #.jpg
                    
            if(format !=None):
                stringedCounter = str(counter)
                print(stringedCounter + format)
                try:
                    with open(stringedCounter + format, 'wb') as f:
                            print('Writing: ', stringedCounter + format)
                            f.write(im.content) 
                            f.close
                            counter=counter+1
                except:
                    print(stringedCounter)
                        #scrivere un file di log
                    pass
        else:
            print("URL: %s " +str(im.status_code),url)     
        return counter
        


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