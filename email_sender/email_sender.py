import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_email(config, recipient_email, subject, message, sending_emails_id):
    """
    Envia um email para o destinatário especificado.
    """
    try:
        server = smtplib.SMTP(config['server_smtp'], config['porta_smtp'])
        server.starttls()
        server.login(config['sender_email'], config['password'])

        msg = MIMEMultipart('alternative')
        msg['From'] = config['sender_email']
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Formatar o corpo do email como HTML
        html_message = f"""
        <html>
        <body>
            <p>{message}</p>
            <div style="width: 100%; height: 50px; background-color: black;"></div>
            <img src="https://b9d8-2804-d55-7906-c00-1470-7fc5-928-8cbe.ngrok-free.app/track_open/{sending_emails_id}" alt="" width="1" height="1" />
        </body>
        </html>
        """
        logging.info('Pixel de rastreamento: %s', html_message)

        # Anexar a mensagem HTML ao email
        msg.attach(MIMEText(html_message, 'html'))

        server.sendmail(config['sender_email'], recipient_email, msg.as_string())
        logging.info('Email enviado com sucesso para: %s', recipient_email)
        server.quit()
        return True
    except Exception as e:
        logging.error('Erro ao enviar email: %s', e)
        return False