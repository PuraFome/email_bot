from flask import Blueprint, jsonify, current_app
import logging

from db.db_connection import connect_db
from apis.utils.db_helpers import fetch_rows, close_connection

email_returns_bp = Blueprint('email_returns', __name__)


@email_returns_bp.route('/api/email_returns', methods=['GET'])
def list_email_returns():
    config = current_app.config
    conn, cursor = connect_db(config)
    if not conn or not cursor:
        return jsonify({'error': 'Erro ao conectar ao banco de dados'}), 500

    rows = fetch_rows(cursor, 'SELECT * FROM marketing."Email_Return_Information" ORDER BY email_opned_date DESC')
    close_connection(conn, cursor)
    return jsonify(rows or []), 200
