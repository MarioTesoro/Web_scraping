from scraper import start_scraper
import os
import traceback
import sys
import threading
from utils.parser import args_parser, url

def main():
    #tempo massimo di durata dello scroll, va inserito per avere una soglia minima di sicurezza
    #safetytime = 60
    #tempo di attesa caricamento pagina ,dipende dalla qualità della rete...
    #loadingtime = 7
    #variabile che indica un valore massimo per il deep scraping di pagine annidate
    #maxNumberOfPages=100000
    #grado di dettaglio del report
    #detail=False

    urls,output,safetytime,loadingtime,maxNumberOfPages,browser= args_parser()
    print(urls,output,safetytime,loadingtime,maxNumberOfPages)
    detail= False
    #scraping
    print(urls)
    start_scraper(urls,output,safetytime,loadingtime,detail,maxNumberOfPages,browser)  

if __name__ == '__main__':    
    try:
        main()
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise
    except:
        traceback.print_exc()
    finally:
        # Reference: http://stackoverflow.com/questions/1635080/terminate-a-multi-thread-python-program
        if threading.active_count() > 1:
            os._exit(getattr(os, "_exitcode", 0))
        else:
            sys.exit(getattr(os, "_exitcode", 0))