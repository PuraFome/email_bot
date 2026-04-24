import logging


def fetch_rows(cursor, query, params=None):
    try:
        cursor.execute(query, params or ())
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    except Exception as e:
        logging.error('Erro ao buscar dados: %s', e)
        try:
            cursor.connection.rollback()
        except Exception:
            pass
        return None


def close_connection(conn, cursor):
    try:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    except Exception as e:
        logging.error('Erro ao fechar conexão de banco de dados: %s', e)
