from datetime import datetime
import uuid
from flask import Blueprint, jsonify, request, send_file, current_app
import pytz
from db.db_connection import connect_db
import logging
import io

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track_open/<sending_id>', methods=['GET'])
def track_open(sending_id):
    """
    Endpoint para rastrear a abertura de emails.
    """
    token = request.args.get('token')
    if not token:
        logging.error('Token não fornecido')
        return jsonify({'error': 'Token nao fornecido'}), 400
    
    config = current_app.config
    conn, cursor = connect_db(config)
    if conn and cursor:
        try:
            cursor.execute("""
                SELECT s.sended_token FROM marketing."Sending" s 
                WHERE s.sending_id = %s AND s.sended_token = %s AND s.sended_token_used = FALSE            
            """, (sending_id, token))
            result = cursor.fetchone()
            if not result:
                logging.error('Token inválido')
                return jsonify({'error': 'Token invalido'}), 400
            
            tz = pytz.timezone('America/Sao_Paulo')
            now_brasilia = datetime.now(tz)
            now_brasilia_naive = now_brasilia.replace(tzinfo=None)
            
            logging.info('hora de abertura do email: %s', now_brasilia)
            unique_id = str(uuid.uuid4())
            cursor.execute("""
                INSERT INTO marketing.email_return_information (email_return_information_id, sending_id, email_opned, email_opned_date)
                VALUES (%s, %s, %s, %s)               
            """, (unique_id, sending_id, True, now_brasilia_naive))
            
            cursor.execute("""
                UPDATE marketing."Sending" SET sended_token_used = TRUE WHERE sending_id = %s
            """, (sending_id,))
            conn.commit()
            logging.info('Abertura de email registrada com sucesso para o ID: %s', sending_id)
        except Exception as e:
            logging.error('Erro ao registrar abertura de email: %s', e)
        finally:
            cursor.close()
            conn.close()

    # Retorne um pixel transparente
    pixel = io.BytesIO()
    pixel.write(b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xFF\xFF\xFF\x21\xF9\x04\x01\x00\x00\x00\x00\x2C\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x4C\x01\x00\x3B')
    pixel.seek(0)
    return send_file(pixel, mimetype='image/gif')