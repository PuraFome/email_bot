from flask import Blueprint, jsonify, current_app
import logging

from db.db_connection import connect_db
from apis.utils.db_helpers import fetch_rows, close_connection

sendings_bp = Blueprint('sendings', __name__)


@sendings_bp.route('/api/sendings', methods=['GET'])
def list_sendings():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    rows = fetch_rows(cursor, 'SELECT * FROM marketing."Sending" ORDER BY sended_email_date DESC')
    close_connection(conn, cursor)
    return jsonify(rows or []), 200


@sendings_bp.route('/api/sendings/<sending_id>', methods=['DELETE'])
def delete_sending(sending_id):
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor.execute(
            'DELETE FROM marketing."Sending" WHERE sending_id = %s',
            (str(sending_id),)
        )
        if cursor.rowcount == 0:
            conn.rollback()
            return jsonify({'error': 'Sending não encontrado'}), 404
        conn.commit()
        return jsonify({'message': 'Sending excluído com sucesso.'}), 200
    except Exception as e:
        logging.error('Erro ao excluir sending: %s', e)
        try:
            conn.rollback()
        except Exception:
            pass
        return jsonify({'error': 'Erro ao excluir sending'}), 500
    finally:
        close_connection(conn, cursor)
