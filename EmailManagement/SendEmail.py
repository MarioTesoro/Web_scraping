import os                                #libreria per gestire sistema operativo
import smtplib                           #libreria per inviare email
from email.message import EmailMessage   #libreria per formatazzione email
from decouple import config              #libreria per prendere dati sensibili da file .env

#in questo metodo viene inviata una mail di notifica, per l'inserimento da parte di un ente di nuovi URL
def send_email(urls,creds):
    host = 'smtp.gmail.com'

    email_address = config('EMAIL')
    email_password = config('EMAILPASSWORD')
    msg = EmailMessage()
    msg['Subject'] = f'segnalazione effettuata da {creds}'
    msg['From'] = email_address
    msg['To'] = 'zorbasimpson@gmail.com'
    msg.set_content(f'Sono stati inseriti nuovi URL nel file master da {creds} e sono:\n\n'+'\n'.join(str(url) for url in urls))

    with smtplib.SMTP_SSL(host) as smtp:
        smtp.login(email_address,email_password)
        smtp.send_message(msg)
