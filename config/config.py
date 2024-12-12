import logging
from dotenv import load_dotenv
import os

def load_config():
    load_dotenv()
    config = {
        'server_smtp': os.getenv('SERVER_SMTP'),
        'porta_smtp': os.getenv('PORTA_SMTP'),
        'sender_email': os.getenv('SENDER_EMAIL'),
        'password': os.getenv('PASSWORD'),
        'range_days': os.getenv('RANGE_DAYS'),
        'database_url': os.getenv('DATABASE_URL')
    }
    logging.info('database_url: %s', config['database_url'])
    return config