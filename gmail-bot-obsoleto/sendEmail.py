import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, TypedDict
import uuid
from dotenv import load_dotenv
import os
import psycopg2

class Enterprise(TypedDict):
    enterprise_meling_id: str
    fantasy_name: str
    email: str

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações do servidor SMTP
server_smtp = os.getenv('SERVER_SMTP')
porta_smtp = os.getenv('PORTA_SMTP')
sender_email = os.getenv('SENDER_EMAIL')
password = os.getenv('PASSWORD')
range_days = os.getenv('RANGE_DAYS')

# Configurações do banco de dados PostgreSQL
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Conectar ao banco de dados
try:
    conn = psycopg2.connect(
        host=db_host,
        port=db_port,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()  
    print('Conexão com o banco de dados realizada com sucesso!')
    
    # Executa a consulta SQL para obter os emails
    cursor.execute(f"""
        select enterprise_meling_id, fantasy_name, email from marketing."Enterprise_Meling" 
        where coontact_valid = true 
        and lower(situation) = 'ativa'
        and enterprise_meling_id not in (
            select enterprise_meling_id from marketing."Sending_Emails" se where created_at >= current_date - interval '{range_days} days'
        )           
    """)
    records = cursor.fetchall()
    enterprises: List[Enterprise] = [{'enterprise_meling_id':record[0],'fantasy_name': record[1], 'email': record[2]} for record in records] 
    print('Empresas:', enterprises)
    
except Exception as e:
    print('Erro ao conectar ao banco de dados:', e)
    enterprises = []
    


 
#Configurações do email
# reciver_email_list = ['samuelpe06062000@gmail.com', 'Erickcelestimo@gmail.com', 'jhonatanknox1@gmail.com']
subject = 'Teste de envio de email com Python'
message = """
Salve mano, este é um teste de envio de email com Python
"""

server = smtplib.SMTP(server_smtp, porta_smtp)
server.starttls()

server.login(sender_email, password)

for enterprise in enterprises:
    #Criando mensagem do email
    message = f"""
    Olá {enterprise['fantasy_name']}, este é um teste de envio de email com Python
    """
    
    #Criando o objeto do email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = enterprise['email']
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    
    #Conectando ao servidor SMTP
    
    try:
        
        text = msg.as_string()
        server.sendmail(sender_email, enterprise['email'], text)
        print('Email enviado com sucesso!')
        
    except Exception as e:
        print('Erro ao enviar email:', e)
        
    finally:
        print('email enviado para:', enterprise['email'])
        
    try:
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        cursor.execute(f"""
            insert into marketing."Sending_Emails" (sending_emails_id, enterprise_meling_id, sender_email, sended_email)
            values ('{unique_id_str}', '{enterprise['enterprise_meling_id']}', '{sender_email}', true)
        """)
        conn.commit()
        print('Email registrado no banco de dados')
    except Exception as e:
        print('Erro ao registrar email no banco de dados:', e)
    
        
        
    
#Fechando a conexão com o servidor SMTP
print('Fechando a conexão com o servidor SMTP')
server.quit()
print('fechando conexão com o banco de dados')
cursor.close()
