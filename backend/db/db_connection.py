import psycopg2
import logging

def connect_db(config):
    try:
        conn = psycopg2.connect(config['database_url'])
        cursor = conn.cursor()
        logging.info('database_url: %s', config['database_url'])
        logging.info('Conexão com o banco de dados realizada com sucesso!')
        return conn, cursor
    except Exception as e:
        logging.error('Erro ao conectar ao banco de dados: %s', e)
        return None, None