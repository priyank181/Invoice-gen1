import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_confirmation_email(receiver_email, body):
    message = MIMEMultipart()
    sender_email = "priyank181818@gmail.com"  # Enter your address
    password = 'Genesis12345!'
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = 'Confirmation for Training'
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)



def send_invoice_email(invoice_path, college, start_date, end_date):
    receiver_email = 'parik1999@gmail.com'
    subject = "Invoice for the training at " + college
    body = "PFA invoice for the training at {0} conducted from {1} to {2}".format(college, str(start_date),
                                                                                  str(end_date))
    sender_email = "priyank181818@gmail.com"
    password = 'Genesis12345!'

    filename = invoice_path
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        f"attachment; filename= Invoice.pdf",
    )

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email
    message.attach(MIMEText(body, "plain"))
    message.attach(part)
    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
