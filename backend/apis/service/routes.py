from flask import Blueprint, jsonify, request, current_app
import threading
import uuid
import logging

from db.db_connection import connect_db
from email_sender.email_sender import send_email
from apis.utils.db_helpers import close_connection

service_bp = Blueprint('service', __name__)
stop_email_service_flag = threading.Event()


@service_bp.route('/start_email_service', methods=['POST'])
def start_email_service():
    """Inicia o serviço de envio de emails."""
    stop_email_service_flag.clear()
    config = current_app.config

    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json(silent=True) or {}
    html_template_id = data.get('html_template_id')
    html_template = get_html_template(cursor, html_template_id) if html_template_id else None

    enterprises = get_enterprises(cursor, config.get('range_days', 30))
    if enterprises is None:
        close_connection(conn, cursor)
        return jsonify({'error': 'Erro ao buscar empresas no banco de dados'}), 500

    runners = get_runners(cursor)
    if not runners:
        close_connection(conn, cursor)
        return jsonify({'error': 'Nenhum runner com platform = gmail encontrado na tabela marketing.runner'}), 500

    for enterprise in enterprises:
        logging.info('Stop email service flag is set: %s', stop_email_service_flag.is_set())
        if stop_email_service_flag.is_set():
            logging.info('Serviço de envio de emails interrompido.')
            break

        subject = 'Teste de envio de email com Python'
        message = f"Olá {enterprise['fantasy_name']}, este é um teste de envio de email com Python"
        token = str(uuid.uuid4())

        sending_id = log_email_sent(cursor, conn, enterprise, runners, token, html_template_id)
        if not sending_id:
            close_connection(conn, cursor)
            return jsonify({'error': f'Erro ao registrar email no banco de dados para {enterprise["email"]}'}), 500

        success, error_message = send_email(config, enterprise['email'], subject, message, sending_id, runners, token, html_template)
        if not success:
            logging.error('Falha no envio de email para %s: %s', enterprise['email'], error_message)
            close_connection(conn, cursor)
            return jsonify({
                'error': 'Erro ao enviar email',
                'details': error_message,
                'email': enterprise['email']
            }), 500

        logging.info('Email enviado com sucesso para: %s', enterprise['email'])

    close_connection(conn, cursor)
    return jsonify({'message': 'Serviço de envio de emails iniciado'}), 200


@service_bp.route('/stop_email_service', methods=['POST'])
def stop_email_service():
    """Para o serviço de envio de emails."""
    stop_email_service_flag.set()
    return jsonify({'message': 'Serviço de envio de emails parado'}), 200


def get_enterprises(cursor, range_days):
    try:
        cursor.execute(f"""
            SELECT 
                enterprise_meling_id, 
                fantasy_name, 
                email 
            FROM 
                marketing."Enterprise_Meling" 
            WHERE 
                coontact_valid = true 
                AND lower(situation) = 'ativa'
                AND enterprise_meling_id NOT IN (
                    SELECT 
                        enterprise_meling_id 
                    FROM 
                        marketing."Sending" se 
                    WHERE 
                        se.sended_email_date >= current_date - interval '{range_days} days'
                )       
        """)
        records = cursor.fetchall()
        return [{'enterprise_meling_id': record[0], 'fantasy_name': record[1], 'email': record[2]} for record in records]
    except Exception as e:
        logging.error('Erro ao obter empresas: %s', e)
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        return None


def log_email_sent(cursor, conn, enterprise, runners, token, model_id):
    try:
        unique_id_str = str(uuid.uuid4())
        runner_id = runners[0]['runner_id']
        cursor.execute(
            """
            INSERT INTO marketing."Sending" (
                sending_id, 
                enterprise_meling_id, 
                runner_id, 
                sended_email, 
                sended_token, 
                model_id
            ) VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING sending_id
            """,
            (
                unique_id_str,
                enterprise['enterprise_meling_id'],
                runner_id,
                True,
                token,
                model_id
            )
        )
        sending_id = cursor.fetchone()[0]
        conn.commit()
        logging.info('Email registrado no banco de dados para: %s', enterprise['email'])
        return sending_id
    except Exception as e:
        logging.error('Erro ao registrar email no banco de dados: %s', e)
        try:
            conn.rollback()
        except Exception:
            pass
        return None


def get_runners(cursor):
    try:
        cursor.execute("""
            SELECT 
                runner_id, 
                runner as email 
            FROM 
                marketing.runner r 
            WHERE 
                r.platform = 'gmail'
        """)
        records = cursor.fetchall()
        return [{'runner_id': record[0], 'email': record[1]} for record in records]
    except Exception as e:
        logging.error('Erro ao obter runners: %s', e)
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        return []


def get_html_template(cursor, template_id):
    try:
        cursor.execute("""
            SELECT 
                html 
            FROM 
                marketing.models 
            WHERE 
                model_id = %s
        """, (str(template_id),))
        record = cursor.fetchone()
        return record[0] if record else None
    except Exception as e:
        logging.error('Erro ao obter modelo HTML: %s', e)
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        return None
