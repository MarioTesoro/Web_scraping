import tkinter as tk                 #librerie per la GUI
from tkinter import filedialog       ###
from tkinter import messagebox       ####
from tkinter import simpledialog     ####
import os                            #libreria per interagire con il SO
import magic                         #libreria per analizzare la natura di un file
                                     #e individuare file con un'estensione non vera
from EmailManagement  import Inbox                         #necessario per poter estrarre URL dalle Email
from ImportingFiles   import FromExcelOrCsv                #necessario per poter estrarre URL da file .xlsx e .csv
from ImportingFiles   import FromTxtOrDocx                 #necessario per poter estrarre URL da file .docx e .txt
from ReportManagement import WritingOnCsv                  #necessario per poter scrivere gli URL sul file .csv 
import re                            #libreria per controllare l'url inserito da input utente
from decouple import config          #libreria per prendere dati sensibili da file .env
from GUI.ExternalGUI import guiRegistration, main_menu,guiInsertCode    #libreria per la gui di registrazione iniziale
from Model.Email import Email        #classe model per email
from EmailManagement import SendEmail                    #necessario per inviare la mail di notifica
from Scrape_and_analyze import scrape_and_analyze, analyzedText

def OKfile(filename,text):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w",encoding="utf-8") as f:
            f.write(text) 
        f.close()
    # Do something with the file
    except IOError:
        print("File not accessible")
        return False

#metodo che controlla se il path dell'email è conforme allo standard
def checkEmail(email):
    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        return False

if __name__ == '__main__':
    #dopo l'importazione dei dati parte lo scraping dei siti nel Master.csv
    #e l'analisi dei contenuti scaricati
    if os.path.exists(os.getcwd()+os.path.sep+"BigFile.csv"):
        analyzedText()
    else:

        #costanti per i message box di errore, su file Maste già aperto
        type_error_document = 'Documento aperto'
        string_error_document = 'Chiudi il file e successivamente prova a caricare i tuoi URL'
        type_url_error = 'errore URL'
        string_error_url ='URL già salvato/i'
        serlab = 's.e.r.l.a.b.'
        type_url_not_found = 'Nessun URL trovato'
        string_url_not_found = 'Nessun URL trovato all\'interno del documento'

        check_gui = True

        while check_gui == True: 
            #GUI di scelta per come approcciare l'app, se da ente che effettua il report o da polizia postale
            #che acquisisce i dati
            check_menu = ''
            menu_flag = True
            while menu_flag == True:
                check_menu = main_menu()
                if type(check_menu) == list:
                        menu_flag = False
                        log_as = check_menu[0]
                elif check_menu == None:
                    exit()

            creds = ''
            #GUI che si occupa di acquisire le informazioni dell'ente che sta effettuando il report
            #degli URL
            if log_as == 'guest':
                check_creds = []
                creds_flag = True
                #sino a quando non vengono inserite le informazioni,tra cui l'email scritta in modo corretto
                #non permette di andare avanti
                while creds_flag == True:
                    check_creds = guiRegistration()
                    if type(check_creds) == list and check_creds[0] != 'back':
                            emailvalidation = checkEmail(check_creds[0])
                            if check_creds[0] != '' and check_creds[1] != '' and emailvalidation == True:
                                creds_flag = False
                                check_gui = False
                                creds = str(check_creds[1] + ', ' + check_creds[0])
                    #esce nel caso in cui viene premuta la x in alto a destra alla finestra
                    elif check_creds == None:
                        exit()
                    #torna al menu se viene premuto il tasto indietro
                    elif check_creds[0] == 'back':
                        creds_flag = False 

            #GUI che si occupa di acquisire un codice per accedere come polizia postale
            elif log_as == 'admin':
                check_creds = []
                creds_flag = True
                #sino a quando non viene inserito il codice corretto per accedere alle impostazioni per la polizia postale
                #non permette di andare avanti
                while creds_flag == True:
                    check_creds = guiInsertCode()
                    if type(check_creds) == list and check_creds[0] != 'back':
                            if check_creds[0] != '' and check_creds[0] == config('CODEPOLIZIAPOSTALE'):
                                creds_flag = False
                                check_gui = False
                                creds = serlab
                    #esce nel caso in cui viene premuta la x in alto a destra alla finestra
                    elif check_creds == None:
                        exit()
                    #torna al menu se viene premuto il tasto indietro
                    elif check_creds[0] == 'back':
                        creds_flag = False

        ################################################################################################
        #costanti per la grandezza della finestra dell'app
        app_width = 500
        app_height = 300

        #definizione della GUI per acquisizione URL
        root= tk.Tk()
        root.title('IMPORT DATI')
        root.option_add('*Entry*background', 'white')
        root.resizable(False, False)
        #permette di chiudere la GUI dal tasto in alto a destra
        root.protocol("WM_DELETE_WINDOW", root.destroy)
        #permette di chiudere la GUI tramire il pulsante Esc
        root.bind('<Escape>', lambda e: root.destroy())

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        x = (screen_width / 2) - (app_width / 2)
        y = (screen_height / 2) - (app_height / 2)

        root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
        #path del file 'Master'  dove vengono memorizzati tutti i dati provenienti
        #dagli altri file
        fileMaster = 'Master.csv'

        ########################GENERAL METHODS##################################

        #metodo per selezionare un file dal computer
        def loadFile():
            #da qui si ottiene il path del file(solo txt, xlsx, csv e docx)
            filepath = filedialog.askopenfilename(initialdir='/',title='Select File',
                                            filetypes=(('Files','*.txt'),('Files','*.xlsx'),('Files','*.csv'),('Files','*.docx')))
            #da qui si ottiene il nome del file selezionato, ottenuto dal path
            filename = os.path.basename(filepath)
            #se non viene selezionato nulla viene mostrato un errore e non viene concesso di procedere
            if filepath == '':
                tk.messagebox.showinfo('Nessun File selezionato','Nessun file o cartella selezionata')
                return False
            return filename,filepath

        #metodo utilizzato per capire che tipo di file l'utente ha caricato, per effettuare i dovuti caricamenti
        #nel file csv
        def typeOfFyle():
            #qui viene chiamato il metodo per far selezionare all'utente il file
            file = loadFile()
            #se non è stato selezionato un file non continua
            if file != False:
                #viene preso il path del file 
                filepath = file[1]
                #il nome del file per per suddividerlo
                #e distinguere un csv da un txt
                #per gli altri documenti non serve
                filename = file[0]
                nameAndExtension = filename.split('.')
                #e viene controllata la tipologia di file
                mime = magic.Magic(mime = True)
                typeofdoc = mime.from_file(filepath)
                #questa poi viene poi utilizzata per chiamare il metodo 
                #per il relativo caricamento dei dati e per evitare che vengano caricati
                #documenti non utilizzabili
                #passando il path del file selezionato
                if(typeofdoc == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
                    transferDocx(file[1])
                elif (nameAndExtension[1] == 'txt' and typeofdoc =='text/plain'):
                    transferTxt(file[1])
                elif (typeofdoc == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
                    transferExcel(file[1])
                elif (nameAndExtension[1] == 'csv' and typeofdoc == 'text/plain'):
                    transferCsv(file[1])

        #####################################STARTS GUI####################################

        canvas1 = tk.Canvas(root, height=300, width=500, bg='#263D42', relief = 'raised')
        canvas1.pack()

        label1 = tk.Label(root, text='Carica i tuoi URL', bg='#263D42')
        label1.config(font=('helvetica', 20))
        canvas1.create_window(250, 50, window=label1)

        ##############################URL FROM FILES METHODS#########################################

        #########DOCX#############
        #########
        ######

        #stampa un messaggio di errore se il file CSV è aperto
        #poichè con il file aperto viene sollevata un'eccezione
        #oppure se gli url sono già stati memorizzati
        def statusFile(status,urls):
            
            #se è aperto mostra un messaggio di errore
            if status == False:
                tk.messagebox.showinfo(type_error_document,string_error_document)
            #se gli url sono già stati salvati mostra un errore
            elif status == 'alreadyIn':
                tk.messagebox.showinfo(type_url_error,string_error_url,icon = 'warning')
            else:
                tk.messagebox.showinfo('Caricamento Completato','Documento caricato')
                #se è un ente ad inserire gli URL invia una mail di notific
                if creds != serlab:
                    SendEmail.send_email(urls,creds) 
                OKfile('importStatus.txt','done')
                root.quit()
                
                

        #metodo per trasferire URL da un file Word a un CSV
        def transferDocx(filepath):
            urls = FromTxtOrDocx.takeUrlFromDocx(filepath)
            #se ha trovato URL scrive
            if len(urls) > 0:
                status = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                #controlla se il file csv è aperto o meno
                statusFile(status,urls)
            #altrimenti mostra errore
            else:
                tk.messagebox.showinfo(type_url_not_found,string_url_not_found)
            

        ###########TXT###########
        #######
        #####

        #metodo per trasferire URL da un file TXT ad un CSV
        def transferTxt(filepath):
            urls = FromTxtOrDocx.takeUrlFromTxt(filepath)
            #se ha trovato URL scrive
            if len(urls) > 0:
                status = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                #controlla se il file csv è aperto o meno
                statusFile(status,urls)
            #altrimenti mostra errore
            else:
                tk.messagebox.showinfo(type_url_not_found,string_url_not_found)
            

        ###############EXCEL############
        ###########
        #####

        #metodo per trasferire URL da un file EXCEL ad un CSV
        def transferExcel(filepath):
            urls = FromExcelOrCsv.moveFromExcel(filepath)
            #se ha trovato URL scrive
            if len(urls) > 0:
                status = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                os.remove('Temporary.csv')
                #controlla se il file csv è aperto o meno
                statusFile(status,urls)
            #altrimenti mostra errore
            else:
                tk.messagebox.showinfo(type_url_not_found,string_url_not_found)
            

        ##############CSV#############
        #########
        ######

        #metodo per trasferire URL da un file CSV ad un CSV
        def transferCsv(filepath):
            urls = FromExcelOrCsv.moveFromCsv(filepath)
            #se ha trovato URL scrive
            if len(urls) > 0:
                status = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                #controlla se il file csv è aperto o meno
                statusFile(status,urls)
            #altrimenti mostra errore
            else:
                tk.messagebox.showinfo(type_url_not_found,string_url_not_found)
            


        #Button for files
        UrlFromFiles = tk.Button(text="              Preleva URL da File               ",
                                        bg='green', fg='white', font=('helvetica', 12, 'bold'),
                                        command=typeOfFyle)
        canvas1.create_window(250, 100, window=UrlFromFiles)

        ##############################URL FROM EMAIL METHODS#########################################

        #metodo utilizzato per trasferire gli URL presenti all'interno di determinate email, nella proprio
        #casella di posta
        def transferEmail():
            urls = []
            status_code = True
            email_obj = Email()
            email_info = Inbox.transferFromEmail()
            if type(email_info) == list and len(email_info) > 0:
                for email in email_info:
                    email_obj = email
                    urls = email_obj.get_urls()
                    creds = email_obj.get_sender()
                    #se è una lista piena scrive gli URL se è possibile
                    if type(urls) == list and len(urls) > 0:
                        #se il file csv su cui scrivere è chiuso, effettua il trasferimento
                        status_code = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                #se lo status code è True, trasferimento con successo
                if status_code == True:
                        tk.messagebox.showinfo('Login andato a buon fine','URL caricati con successo')
                        OKfile('importStatus.txt','done')
                        root.quit()
                #altrimenti se è alreadyIn gli URL son già stati salvati e mostra un errore
                elif status_code == 'alreadyIn':
                        tk.messagebox.showinfo(type_url_error,'Alcuni URL erano già stati salvati',icon = 'warning') 
                        OKfile('importStatus.txt','done')
                        root.quit()
                #altrimenti mostra un messaggio di errore, per documento aperto
                else:
                        tk.messagebox.showinfo(type_error_document,string_error_document)
            else:
                tk.messagebox.showinfo('Errore Inbox','Nessuna email con URL trovata negli ultimi 7 giorni',icon = 'warning')

        #Bottone per email, accessibile solo dalla polizia postale
        if(creds == serlab):
            UrlFromEmail = tk.Button(text="           Preleva URL dall'email             ", command= transferEmail,
                                            bg='green', fg='white', font=('helvetica', 12, 'bold'))
            canvas1.create_window(250, 150, window=UrlFromEmail)

        ##############################URL FROM EMAIL METHODS#########################################

        #metodo utilizzato per acquisire URL da input utente, tramite GUI
        #e scriverlo all'interno del file
        def transferInput():
            urls = []
            #dialog per richiesta dell'URL
            url = simpledialog.askstring(title="URLInput",
                                        prompt="Inserisci l'URL: ", parent = root)
            #l'url viene poi inserito in una lista per poterlo poi passare
            #al metodo che si occupa di effettuare la scrittura
            urls.append(url)
            if url != '' and url != None:
                regex = re.compile(
                    r'^(?:http|ftp)s?://' # http:// or https://
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                    r'localhost|' #localhost...
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                    r'(?::\d+)?' # optional port
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                #viene controllato che l'input dell'utente sia effettivamente un URL prima di poterlo inserire
                #nel file csv. Sia in caso di erroe che di inserimento corretto viene mostrato un feedback testuale
                if((re.match(regex, url) is not None) == False):
                    tk.messagebox.showinfo('Errore Input','URL sbagliato',icon = 'warning')
                else:
                    #se il file csv su cui scrivere è chiuso, effettua il trasferimento
                    status_code = WritingOnCsv.writingIntoCsv(fileMaster,urls,creds)
                    if status_code == True:
                        tk.messagebox.showinfo('Input andato a buon fine','URL caricato')
                        #se è un ente ad inserire gli URL invia una mail di notifica
                        if creds != serlab:
                            SendEmail.send_email(urls,creds)
                        OKfile('importStatus.txt','done')
                        root.quit()
                    #altrimenti controlla che gli URL, non siano già stati salvati, se è così mostra un errore
                    elif status_code == 'alreadyIn':
                        tk.messagebox.showinfo(type_url_error,string_error_url,icon = 'warning')
                    #altrimenti mostra un messaggio di errore
                    else:
                        tk.messagebox.showinfo(type_error_document,string_error_document)
            else:
                    tk.messagebox.showinfo('Input non valido','Nessun input rilevato',icon = 'warning')

        #Bottone per input, che viene spostato se l'accesso è fatto da un ente
        if(creds == serlab):
            UrlFromInput = tk.Button(text="           Preleva URL da input            ",
                                            bg='green', command= transferInput, fg='white', font=('helvetica', 12, 'bold'))
            canvas1.create_window(250, 200, window=UrlFromInput)
        else:
            UrlFromInput = tk.Button(text="            Preleva URL da input             ",
                                        bg='green', command= transferInput, fg='white', font=('helvetica', 12, 'bold'))
            canvas1.create_window(250, 150, window=UrlFromInput)

        ################METHOD AND GUI FOR EXIT APPLICATION##########################
            
        def exitApplication():
            msg_box = tk.messagebox.askquestion ('Esci dall\'Applicazione','Sei sicuro di voler uscire?',icon = 'warning')
            if msg_box == 'yes':
                OKfile('importStatus.txt','closed')
                root.quit()
                
                

        #Bottone per uscire dall'app, che viene spostato se l'accesso è fatto da un ente
        if(creds == serlab):
            exitButton = tk.Button (root, text='        Esci dall\'Applicazione      ', bg='red', fg='white', font=('helvetica', 12, 'bold'),
                                    command=exitApplication)
            canvas1.create_window(250, 250, window=exitButton)
        else:
            exitButton = tk.Button (root, text='        Esci dall\'Applicazione      ', bg='red', fg='white', font=('helvetica', 12, 'bold'),
                                    command=exitApplication)
            canvas1.create_window(250, 200, window=exitButton)

        root.mainloop()

        scrape_and_analyze()
        analyzedText()

    os.remove("BigFile.csv")