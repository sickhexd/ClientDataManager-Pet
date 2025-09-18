# auth_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string

def auth_code(size=6, chars=string.ascii_uppercase + string.digits):
    code = ''.join(random.choice(chars) for _ in range(size))
    return code

def send_email(subject, body, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'sabiaflex0@gmail.com'
    sender_password = 'nrkz adbu zkwo yeoz'
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        print(f"Email отправлен на {to_email}")
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")

def generate_and_send_code(email):
    code = auth_code()
    send_email("Auth Code", f"Your authentication code is: {code}", email)
    print(f"Код отправлен на {email}")
    return code
