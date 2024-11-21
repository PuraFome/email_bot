import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

from db.db_connection import connect_db

def send_email(config, recipient_email, subject, message, sending_id, runners, token):
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
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@600&display=swap" rel="stylesheet">
            <style>
                body {{
                    font-family: 'Roboto', sans-serif;
                    color: #fff;
                    text-align: left;
                    padding: 0;
                    margin: 0;
                    background-color: black;
                }}
                .container {{
                    padding: 20px;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .logo {{
                    width: 150px;
                    margin-bottom: 20px;
                    display: block;
                    margin-left: auto;
                    margin-right: auto;
                }}
                .main-text {{
                    font-size: 32px;
                    font-weight: 600;
                    margin-bottom: 10px;
                    text-align: left;
                    color: #fff;
                }}
                .highlight {{
                    color: red;
                    display: block;
                    width: 100%;
                }}
                .sub-text {{
                    font-size: 18px;
                    margin-bottom: 20px;
                    color: #fff;
                    text-align: left;
                }}
                .example-image {{
                    width: 100%;
                    max-width: 600px;
                    margin-bottom: 20px;
                }}
                .info-text {{
                    font-size: 16px;
                    margin-bottom: 20px;
                    color: #fff;
                    text-align: left;
                }}
                .button {{
                    display: inline-block;
                    margin-top: 20px;
                }}
                .button img {{
                    width: 200px;
                }}
            </style>
        </head>
        <body>
            <table width="80%" cellpadding="0" cellspacing="0" border="0" style="background-color: black;">
                <tr>
                    <td align="center">
                        <div class="container">
                            <img src="https://storage.googleapis.com/pure-digital-us/runners/LOGO_P.png" alt="Pure Digital Logo" class="logo" />
                            <div class="main-text">Sua Landing Page Precisa Ser</div>
                            <div class="main-text highlight">Tão Única Quanto o Seu Negócio</div>
                            <div class="sub-text">Landing Pages Exclusivas para Aumentar a Visibilidade e Confiança do Seu Negócio Online</div>
                            <img src="https://storage.googleapis.com/pure-digital-us/runners/LPS.png" alt="Exemplos de Landing Page" class="example-image" />
                            <div class="info-text">Quer saber o que é uma Landing Page e como ela pode transformar seu negócio?</div>
                            <a href="https://wa.me/44984574871" class="button">
                                <img src="https://storage.googleapis.com/pure-digital-us/runners/BOTAO.png" alt="Botão WhatsApp" />
                            </a>
                            <div class="info-text">este email está usando a font roboto</div>
                        </div>
                    </td>
                </tr>
            </table>
            <img src="https://malling-bot-2-935702226305.southamerica-east1.run.app/track_open/{sending_id}?token={token}" alt="" width="1" height="1" />
        </body>
        </html>
        """
        
        # Anexar a mensagem HTML ao email
        msg.attach(MIMEText(html_message, 'html'))

        server.sendmail(email, recipient_email, msg.as_string())
        logging.info('Email enviado com sucesso para: %s', recipient_email)
        server.quit()
        return True
    except Exception as e:
        logging.error('Erro ao enviar email: %s', e)
        return False
    

