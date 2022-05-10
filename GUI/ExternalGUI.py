#PROVE PER GRAFICA MIGLIORE LOG IN EMAIL E INSERIMENTO URL

import tkinter as tk                    #librerie per la GUI
from tkinter import filedialog          ####
from tkinter import messagebox          ###

Escape = '<Escape>'

#GUI per la registrazione della società
def guiRegistration():
   creds = []
   app_width = 500
   app_height = 300

   rootLog= tk.Tk()
   rootLog.title('Registrazione')
   rootLog.resizable(False, False)
   #permette di chiudere la GUI dal tasto in alto a destra
   rootLog.protocol("WM_DELETE_WINDOW", rootLog.destroy)
   #permette di chiudere la GUI tramire il pulsante Esc
   rootLog.bind(Escape, lambda e: rootLog.destroy())

   screen_width = rootLog.winfo_screenwidth()
   screen_height = rootLog.winfo_screenheight()

   x = (screen_width / 2) - (app_width / 2)
   y = (screen_height / 2) - (app_height / 2)

   rootLog.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

   email_input = tk.StringVar(rootLog)
   company_name_input = tk.StringVar(rootLog)

   canvas1 = tk.Canvas(rootLog, height=app_height, width=app_width, bg='#263D42', relief = 'raised')
   canvas1.pack()

   label1 = tk.Label(rootLog, text='Chi sta effettuando il report?', bg='#263D42')
   label1.config(font=('helvetica', 20))
   canvas1.create_window(250, 50, window=label1)

   emailLabel = tk.Label(rootLog, text='E-mail', bg='#263D42')
   emailLabel.config(font=('helvetica', 15))
   canvas1.create_window(240, 90, window=emailLabel)

   emailEntry = tk.Entry(rootLog, bg='white', width=25, textvariable=email_input)
   emailEntry.config(font=('helvetica', 15))
   canvas1.create_window(240, 120, window=emailEntry)

   companyLabel = tk.Label(rootLog, text='Nome compagnia', bg='#263D42')
   companyLabel.config(font=('helvetica', 15))
   canvas1.create_window(240, 160, window=companyLabel)

   companyEntry = tk.Entry(rootLog, bg='white', width=25, textvariable=company_name_input)
   companyEntry.config(font=('helvetica', 15))
   canvas1.create_window(240, 190, window=companyEntry)

   loginButton = tk.Button(rootLog, text="  Continua  ", bg='green', fg='white', command=lambda:(lambda x:rootLog.destroy())(creds.extend([emailEntry.get(), companyEntry.get()])) ,
                            font=('helvetica', 12, 'bold'))
   canvas1.create_window(400, 250, window=loginButton)

   back_button = tk.Button(rootLog, text="  Indietro  ", bg='red', fg='white', command=lambda:(lambda x:rootLog.destroy())(creds.append('back')) ,
                            font=('helvetica', 12, 'bold'))
   canvas1.create_window(90, 250, window=back_button)

   rootLog.mainloop()
   return creds if creds else None



#Gui per inserire codice della polizia postale
def guiInsertCode():
   code = []

   app_width = 500
   app_height = 300

   root1= tk.Tk()
   root1.title('Inserire Codice')
   root1.resizable(False, False)
   #permette di chiudere la GUI dal tasto in alto a destra
   root1.protocol("WM_DELETE_WINDOW", root1.destroy)
   #permette di chiudere la GUI tramire il pulsante Esc
   root1.bind(Escape, lambda e: root1.destroy())

   screen_width = root1.winfo_screenwidth()
   screen_height = root1.winfo_screenheight()

   x = (screen_width / 2) - (app_width / 2)
   y = (screen_height / 2) - (app_height / 2)

   root1.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

   code_input = tk.StringVar(root1)
 

   canvas1 = tk.Canvas(root1, height=app_height, width=app_width, bg='#263D42', relief = 'raised')
   canvas1.pack()

   label1 = tk.Label(root1, text='Inserisci il codice per accedere', bg='#263D42')
   label1.config(font=('helvetica', 20))
   canvas1.create_window(240, 60, window=label1)

   code_label = tk.Label(root1, text='CODICE QUI', bg='#263D42')
   code_label.config(font=('helvetica', 15))
   canvas1.create_window(240, 120, window=code_label)

   code_entry = tk.Entry(root1, bg='white', show="*", width=20, textvariable=code_input)
   code_entry.config(font=('helvetica', 15))
   canvas1.create_window(240, 160, window=code_entry)


   insert_button = tk.Button(root1, text="  Continua  ", bg='green', fg='white', command=lambda:(lambda x:root1.destroy())(code.extend([code_entry.get()])) ,
                            font=('helvetica', 12, 'bold'))
   canvas1.create_window(400, 250, window=insert_button)

   back_button = tk.Button(root1, text="  Indietro  ", bg='red', fg='white', command=lambda:(lambda x:root1.destroy())(code.append('back')) ,
                            font=('helvetica', 12, 'bold'))
   canvas1.create_window(90, 250, window=back_button)

   root1.mainloop()
   return code if code else None

#GUI per menu app
def main_menu():
   chooser = []
   app_width = 400
   app_height = 200

   root= tk.Tk()
   root.title('Import')
   root.resizable(False, False)
   #permette di chiudere la GUI dal tasto in alto a destra
   root.protocol("WM_DELETE_WINDOW", root.destroy)
   #permette di chiudere la GUI tramire il pulsante Esc
   root.bind(Escape, lambda e: root.destroy())

   canvas1 = tk.Canvas(root, height=app_height, width=app_width, bg='#263D42', relief = 'raised')
   canvas1.pack()

   screen_width = root.winfo_screenwidth()
   screen_height = root.winfo_screenheight()

   x = (screen_width / 2) - (app_width / 2)
   y = (screen_height / 2) - (app_height / 2)

   root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

   label1 = tk.Label(root, text='inserisci dati come', bg='#263D42')
   label1.config(font=('helvetica', 20))
   canvas1.create_window(200, 50, window=label1)

   guest_button = tk.Button(root, text="      Ente      ", bg='green', fg='white', command=lambda:(lambda x:root.destroy())(chooser.append('guest')),
                           font=('helvetica', 12, 'bold'))
   canvas1.create_window(200, 100, window=guest_button)

   admin_button = tk.Button(root, text="  SERLAB  ", bg='green', fg='white', command=lambda:(lambda x:root.destroy())(chooser.append('admin')), 
                            font=('helvetica', 12, 'bold'))
   canvas1.create_window(200, 150, window=admin_button)
   

   root.mainloop()
   return chooser if chooser else None

