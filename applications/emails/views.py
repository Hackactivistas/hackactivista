from django.shortcuts import render

# Create your views here.
import threading
 
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

import os, time
from datetime import datetime
 
 
class EmailThread(threading.Thread):
    """
    Class para enviar un email con thread.
    """
    def __init__(self, subject, body, from_email, recipient_list,
                 fail_silently, html, attach, file):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.attach = attach
        self.file = file
        threading.Thread.__init__(self)

    def save_log_send(self, email_to, error, intento):
        """
        Almacenamos todos log en archivo, para tener como referencia de todo el trazado del proceso de descarga   
        """
        f = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/log/send-emails.txt', 'a')
        mensaje = "Messaje: " + email_to + " : " + error + " : " + str(intento) + " : " + datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        f.write('\n' + mensaje)
        f.close()
        return
 
    def run(self):
        msg = EmailMultiAlternatives(
            self.subject, self.body, self.from_email, self.recipient_list
        )
 
        # Si es en formato html
        if self.html:
            msg.attach_alternative(self.html, "text/html")
 
        # Si adjunta un archivo
        if self.attach:
            fp = open(self.file, 'rb')
            # muy importante MIMEApplication para adjuntar PDF, MIMEBase no soporta
            # envio de PDF
            lista_nombre_adjunto = self.file.split('/')
            nombre_adjunto = lista_nombre_adjunto[len(lista_nombre_adjunto)-1]
            adjunto = MIMEApplication(fp.read(), _subtype="pdf")
            # print ('adjunto:', adjunto.__dict__)
            fp.close()
            adjunto.add_header('Content-Disposition',
                               'attachment', filename=nombre_adjunto)
            # adjuntamos al mensaje
            # msg_image = MIMEImage(self.file.read())
            # msg_image.add_header('Content-ID', '<{}>'.format(
            #     "<" + self.file.name + ">")
            # )
            # msg_image.add_header(
            #     "Content-Disposition", "inline",
            #     filename=self.file.name
            # )
            msg.attach(adjunto)
        
        intento = 0
        while True:
            if intento >= 4:
                self.save_log_send(self.recipient_list[0], "Ha superado el limite de intentos", intento)
                break
            try:
                estatus_send = msg.send(self.fail_silently)
                if estatus_send == 1:
                    print ('Se envio el correo')
                    intento = 4
                    break
            except Exception as e:
                intento +=1
                time.sleep(1)
                self.save_log_send(self.recipient_list[0], str(e), intento)
                print ("Ocurrio un error en el envio de correo:", e)
 
 
def send_mail(subject, body, from_email, recipient_list, fail_silently=False,
              html=None, attach=None, file=None, *args, **kwargs):
    """
    Send email
    """
    EmailThread(
        subject, body, from_email, recipient_list,
        fail_silently, html, attach, file
    ).start()
   