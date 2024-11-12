from flask import Flask, jsonify, request
from config.config import load_config
from db.db_connection import connect_db
from email_sender.email_sender import send_email
from logs.logger import setup_logging
from tracking.tracking import tracking_bp
import uuid
import logging
import threading

app = Flask(__name__)
setup_logging()
config = load_config()
app.config.update(config)

# Registrar o blueprint de rastreamento
app.register_blueprint(tracking_bp)

# Sinalizador global para controlar o loop
stop_email_service_flag = threading.Event()

@app.route('/start_email_service', methods=['POST'])
def start_email_service():
    """
    Inicia o serviço de envio de emails.
    """
    global stop_email_service_flag
    stop_email_service_flag.clear()  # Resetar o sinalizador ao iniciar o serviço

    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    enterprises = get_enterprises(cursor, config['range_days'])
    runners = get_runners(cursor)
    for enterprise in enterprises:
        logging.info('Stop email service flag is set: %s', stop_email_service_flag.is_set())
        if stop_email_service_flag.is_set():
            logging.info('Serviço de envio de emails interrompido.')
            break
        subject = 'Teste de envio de email com Python'
        message = f"Olá {enterprise['fantasy_name']}, este é um teste de envio de email com Python"
        
        token = str(uuid.uuid4())
        
        sending_id = log_email_sent(cursor, conn, enterprise, runners, token)
        if send_email(config, enterprise['email'], subject, message, sending_id, runners, token):
            logging.info('Email enviado com sucesso para: %s', enterprise['email'])

    cursor.close()
    conn.close()
    return jsonify({'message': 'Serviço de envio de emails iniciado'}), 200

@app.route('/stop_email_service', methods=['POST'])
def stop_email_service():
    """
    Para o serviço de envio de emails.
    """
    global stop_email_service_flag
    stop_email_service_flag.set()  # Sinalizar para parar o serviço
    return jsonify({'message': 'Serviço de envio de emails parado'}), 200

def get_enterprises(cursor, range_days):
    """
    Obtém a lista de empresas do banco de dados.
    """
    try:
        cursor.execute(f"""
            SELECT enterprise_meling_id, fantasy_name, email FROM marketing."Enterprise_Meling" 
            WHERE coontact_valid = true 
            AND lower(situation) = 'ativa'
            AND enterprise_meling_id NOT IN (
                SELECT enterprise_meling_id FROM marketing."Sending" se WHERE created_at >= current_date - interval '{range_days} days '
            )       
        """)
        records = cursor.fetchall()
        enterprises = [{'enterprise_meling_id': record[0], 'fantasy_name': record[1], 'email': record[2]} for record in records]
        logging.info('Empresas: %s', enterprises)
        return enterprises
    except Exception as e:
        logging.error('Erro ao obter empresas: %s', e)
        return []

def log_email_sent(cursor, conn, enterprise, runners, token):
    """
    Registra o envio de email no banco de dados e retorna o ID do envio.
    """
    try:
        unique_id = uuid.uuid4()
        unique_id_str = str(unique_id)
        runner_id = runners[0]['runner_id']
        cursor.execute(f"""
            INSERT INTO marketing."Sending" (sending_id, enterprise_meling_id, runner_id, sended_email, sended_token)
            VALUES ('{unique_id_str}', '{enterprise['enterprise_meling_id']}', '{runner_id}', true, '{token}')
            RETURNING sending_id
        """)
        conn.commit()
        logging.info('Email registrado no banco de dados para: %s', enterprise['email'])
        return unique_id_str
    except Exception as e:
        logging.error('Erro ao registrar email no banco de dados: %s', e)
        return None

def get_runners(cursor):
    """
    Obtém a lista de emails que serão usados para o envio do banco de dados.
    """
    try:
        cursor.execute(f"""
            SELECT runner_id, runner as email FROM marketing.runner r 
            WHERE r.platform = 'gmail'
        """)
        records = cursor.fetchall()
        runners = [{'runner_id': record[0], 'email': record[1]} for record in records]
        logging.info('Runners: %s', runners)
        return runners
    except Exception as e:
        logging.error('Erro ao obter runners: %s', e)
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)