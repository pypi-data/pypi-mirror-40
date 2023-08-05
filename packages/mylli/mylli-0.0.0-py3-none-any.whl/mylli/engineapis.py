# key ="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"
#Improvising

import sendgrid
import os
from sendgrid.helpers.mail import *
key ="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"
def send(from_email, to_email, subject, body):

    sg = sendgrid.SendGridAPIClient(apikey=key)
    from_email = Email(from_email)
    to_email = Email(to_email)
    subject = subject
    content = Content("text/plain", body)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)
    return response
