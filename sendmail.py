import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import codecs

fileOpener = open('sendgrid.json')
data = json.load(fileOpener)
fileOpener.close()

recipients = []

for (key, value) in data['recipients'].items():
    recipients.append(value['email'])


def SendMail(sub, content):

    message = Mail(
        from_email=data['sender'],
        to_emails=recipients,
        subject=sub,
        html_content=content)
    try:
        sg = SendGridAPIClient(data['SENDGRID_API_KEY'])
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
