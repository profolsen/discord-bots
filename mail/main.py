import os
import sendgrid
from sendgrid import Personalization

from sendgrid.helpers.mail import Content, Email, Mail

def doIt() :
    sg = sendgrid.SendGridAPIClient(
        api_key=''#os.environ.get("SENDGRID_API_KEY")
    )
    mail = Mail()
    mail.from_email = Email("protsoph@gmail.com")
    mail.subject = "A test email from Sendgrid"
    personalization = Personalization()
    personalization.add_to(Email("olsenp@strose.edu"))
    mail.add_personalization(personalization)
    mail.add_content(Content(
        "text/plain", "Here's a test email\n sent through Python"
    ))
#    mail = Mail(from_email, subject, to_email, content)
    print(mail);
    response = sg.client.mail.send.post(request_body=mail.get())

    # The statements below can be included for debugging purposes
    print(response.status_code)
    print(response.body)
    print(response.headers)

if __name__ == "__main__" :
    doIt()