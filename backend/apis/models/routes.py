from flask import Blueprint, jsonify, request, current_app
import uuid
import logging

from db.db_connection import connect_db
from apis.utils.db_helpers import fetch_rows, close_connection

models_bp = Blueprint('models', __name__)


@models_bp.route('/api/models', methods=['GET'])
def list_models():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    rows = fetch_rows(cursor, 'SELECT * FROM marketing.models ORDER BY created_at DESC')
    close_connection(conn, cursor)
    return jsonify(rows or []), 200


@models_bp.route('/api/models', methods=['POST'])
def create_model():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json(silent=True) or {}
    model_id = data.get('model_id') or str(uuid.uuid4())
    try:
        cursor.execute(
            """
            INSERT INTO marketing.models (
                model_id,
                html,
                created_at,
                updated_at
            ) VALUES (%s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """,
            (model_id, data.get('html'))
        )
        conn.commit()
        close_connection(conn, cursor)
        return jsonify({'message': 'Model criado com sucesso.', 'model_id': model_id}), 201
    except Exception as e:
        logging.error('Erro ao criar model: %s', e)
        conn.rollback()
        close_connection(conn, cursor)
        return jsonify({'error': str(e)}), 500


@models_bp.route('/api/models/<model_id>', methods=['DELETE'])
def delete_model(model_id):
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor.execute('DELETE FROM marketing.models WHERE model_id = %s', (model_id,))
        conn.commit()
        close_connection(conn, cursor)
        return jsonify({'message': 'Model excluído com sucesso.'}), 200
    except Exception as e:
        logging.error('Erro ao excluir model: %s', e)
        conn.rollback()
        close_connection(conn, cursor)
        return jsonify({'error': str(e)}), 500
