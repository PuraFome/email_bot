import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

#Configurações do servidor SMTP
server_smtp = 'smtp.gmail.com'
porta_smtp = 587
sender_email = "agleano02@gmail.com"
password = "hqzjihfrlftymeth"
 
#Configurações do email
reciver_email = 'samuelpe06062000@gmail.com'
subject = 'Teste de envio de email com Python'
message = 'Olá, este é um teste de envio de email com Python'

#Criando o objeto do email
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = reciver_email
msg['Subject'] = subject
msg.attach(MIMEText(message, 'plain'))

#Conectando ao servidor SMTP
try:
    server = smtplib.SMTP(server_smtp, porta_smtp)
    server.starttls()
    
    server.login(sender_email, password)
    
    text = msg.as_string()
    server.sendmail(sender_email, reciver_email, text)
    print('Email enviado com sucesso!')

except Exception as e:
    print('Erro ao enviar email:', e)

finally:
    print('Fechando a conexão com o servidor SMTP')
    server.quit()