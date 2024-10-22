import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_email(config, recipient_email, subject, message):
    try:
        server = smtplib.SMTP(config['server_smtp'], config['porta_smtp'])
        server.starttls()
        server.login(config['sender_email'], config['password'])

        msg = MIMEMultipart()
        msg['From'] = config['sender_email']
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        server.sendmail(config['sender_email'], recipient_email, msg.as_string())
        logging.info('Email enviado com sucesso para: %s', recipient_email)
        server.quit()
        return True
    except Exception as e:
        logging.error('Erro ao enviar email: %s', e)
        return False