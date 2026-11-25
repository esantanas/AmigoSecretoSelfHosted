from gmail_sender import GmailSender
import json
import random

def Revolver(participantes):
    if len(participantes) <2:
        raise ValueError('Se necesitan al menos dos participantes.')

    emails = list(participantes.keys())
    random.shuffle(emails)

    resultado = {}
    for i, email, in enumerate(emails):
        resultado[email] = emails[(i+1) % len(emails)]
    return resultado
 
import json

with open("participantes.json", encoding="utf-8") as f:
    participantes = json.load(f)


resultado = Revolver(participantes=participantes)
mailer = GmailSender(credentials_path = 'credentials.json', token_path='token.json')

for receptor, regalado in resultado.items():
    respuesta = mailer.send_email(
        to = receptor.strip(),
        subject = "Tu amigo secreto es...",
        body= f"Hola! Te informamos que te ha tocado como amigx secreto {participantes[regalado]} cuyo email es {regalado}",
    )

