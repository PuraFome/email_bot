import logging
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

def build_database_url():
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST', 'postgres')
    port = os.getenv('DB_PORT', '5432')
    name = os.getenv('DB_NAME')
    if user and password and name:
        return f"postgresql://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{quote_plus(name)}"
    return None

def load_config():
    load_dotenv()
    database_url = os.getenv('DATABASE_URL') or build_database_url()
    config = {
        'server_smtp': os.getenv('SERVER_SMTP'),
        'porta_smtp': os.getenv('PORTA_SMTP'),
        'sender_email': os.getenv('SENDER_EMAIL'),
        'password': os.getenv('PASSWORD'),
        'range_days': os.getenv('RANGE_DAYS'),
        'database_url': database_url
    }
    logging.info('database_url: %s', config['database_url'])
    return config
