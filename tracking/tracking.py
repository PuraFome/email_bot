from flask import Blueprint, send_file, current_app
from db.db_connection import connect_db
import logging
import io

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/track_open/<sending_emails_id>', methods=['GET'])
def track_open(sending_emails_id):
    """
    Endpoint para rastrear a abertura de emails.
    """
    config = current_app.config
    conn, cursor = connect_db(config)
    if conn and cursor:
        try:
            cursor.execute(f"""
                UPDATE marketing."Sending_Emails"
                SET opened_email = TRUE, opened_email_date = NOW()
                WHERE sending_emails_id = '{sending_emails_id}'
            """)
            conn.commit()
            logging.info('Abertura de email registrada com sucesso para o ID: %s', sending_emails_id)
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