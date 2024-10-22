import psycopg2
import logging

def connect_db(config):
    try:
        conn = psycopg2.connect(
            host=config['db_host'],
            port=config['db_port'],
            database=config['db_name'],
            user=config['db_user'],
            password=config['db_password']
        )
        cursor = conn.cursor()
        logging.info('Conexão com o banco de dados realizada com sucesso!')
        return conn, cursor
    except Exception as e:
        logging.error('Erro ao conectar ao banco de dados: %s', e)
        return None, None