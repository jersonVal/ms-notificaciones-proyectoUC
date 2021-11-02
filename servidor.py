# -*- coding: utf-8 -*-
"""
Created on Mon Nov  1 16:51:04 2021

@author: jeson valencia
"""

from flask import Flask
from flask import request
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from twilio.rest import Client

app = Flask(__name__)

@app.route("/correo")
def enviarCorreo():
    destino = request.args.get('destino')
    asunto = request.args.get('asunto')
    mensaje = request.args.get('mensaje')
    hashString = request.args.get('hash')
    if hashString == os.environ.get('SECURITY_HASH'):
        message = Mail(
            from_email= os.environ.get('Email_from'),
            to_emails= destino,
            subject= asunto,
            html_content = mensaje)
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print('Enviado')
            return 'OK'
        except Exception as e:
            print(e.message)
            return 'KO'
    else:
        print('Hash error')
        return 'KO'
    
@app.route("/sms")
def enviarSms():
    destino = request.args.get('destino')
    mensaje = request.args.get('mensaje')
    hashString = request.args.get('hash')
    if hashString == os.environ.get('SECURITY_HASH'):
        try:
            # and set the environment variables. See http://twil.io/secure
            client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
            
            message = client.messages \
                            .create(
                                 body = mensaje,
                                 from_='+13193673387',
                                 to='+57' + destino
                             )
            
            print(message.sid)
            print('Enviado Sms')
            return 'OK'
        except Exception as e:
            print(e.message)
            return 'KO'
    else:
        print('Hash error')
        return 'KO'
    
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    app.run()

