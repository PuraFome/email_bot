from flask import Blueprint, jsonify, request, current_app
import uuid
import logging

from db.db_connection import connect_db
from apis.utils.db_helpers import fetch_rows, close_connection

enterprise_meling_bp = Blueprint('enterprise_meling', __name__)


@enterprise_meling_bp.route('/api/enterprise_meling', methods=['GET'])
def list_enterprise_meling():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    rows = fetch_rows(cursor, 'SELECT * FROM marketing."Enterprise_Meling" ORDER BY created_at DESC')
    close_connection(conn, cursor)
    return jsonify(rows or []), 200


@enterprise_meling_bp.route('/api/enterprise_meling', methods=['POST'])
def create_enterprise_meling():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    data = request.get_json(silent=True) or {}
    enterprise_id = data.get('enterprise_meling_id') or str(uuid.uuid4())
    try:
        cursor.execute(
            """
            INSERT INTO marketing."Enterprise_Meling" (
                enterprise_meling_id,
                name,
                fantasy_name,
                whatsapp,
                ddd,
                email,
                coontact_valid,
                open_date,
                main_activity_code,
                main_activity_description,
                cnpj,
                situation,
                country,
                created_at,
                region,
                share_capital,
                state
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s)
            """,
            (
                enterprise_id,
                data.get('name'),
                data.get('fantasy_name'),
                data.get('whatsapp'),
                data.get('ddd'),
                data.get('email'),
                data.get('coontact_valid', False),
                data.get('open_date'),
                data.get('main_activity_code'),
                data.get('main_activity_description'),
                data.get('cnpj'),
                data.get('situation'),
                data.get('country'),
                data.get('region'),
                data.get('share_capital'),
                data.get('state')
            )
        )
        conn.commit()
        close_connection(conn, cursor)
        return jsonify({'message': 'Enterprise criado com sucesso.', 'enterprise_meling_id': enterprise_id}), 201
    except Exception as e:
        logging.error('Erro ao criar enterprise: %s', e)
        conn.rollback()
        close_connection(conn, cursor)
        return jsonify({'error': str(e)}), 500


@enterprise_meling_bp.route('/api/enterprise_meling/<enterprise_id>', methods=['DELETE'])
def delete_enterprise_meling(enterprise_id):
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    try:
        cursor.execute('DELETE FROM marketing."Enterprise_Meling" WHERE enterprise_meling_id = %s', (enterprise_id,))
        conn.commit()
        close_connection(conn, cursor)
        return jsonify({'message': 'Enterprise excluído com sucesso.'}), 200
    except Exception as e:
        logging.error('Erro ao excluir enterprise: %s', e)
        conn.rollback()
        close_connection(conn, cursor)
        return jsonify({'error': str(e)}), 500
