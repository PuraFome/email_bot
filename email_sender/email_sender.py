import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

def send_email(config, recipient_email, subject, message, sending_id, runners):
    """
    Envia um email para o destinatário especificado.
    """
    try:
        server = smtplib.SMTP(config['server_smtp'], config['porta_smtp'])
        server.starttls()
        email = runners[0]['email']
        server.login(email, config['password'])

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
            <img src="https://malling-bot-2-935702226305.southamerica-east1.run.app/track_open/{sending_id}" alt="" width="1" height="1" />
        </body>
        </html>
        """
        logging.info('Pixel de rastreamento: %s', html_message)

        # Anexar a mensagem HTML ao email
        msg.attach(MIMEText(html_message, 'html'))

        server.sendmail(email, recipient_email, msg.as_string())
        logging.info('Email enviado com sucesso para: %s', recipient_email)
        server.quit()
        return True
    except Exception as e:
        logging.error('Erro ao enviar email: %s', e)
        return False
    

