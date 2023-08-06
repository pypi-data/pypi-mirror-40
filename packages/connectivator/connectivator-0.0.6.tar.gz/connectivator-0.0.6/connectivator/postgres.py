import os

from sqlalchemy import create_engine


def get_engine(db_name):

    DATA_USERNAME = os.environ['PGUSER']
    DATA_PASSWORD = os.environ['PGPASSWORD']
    DATA_HOSTNAME = os.environ['PGHOST']
    DATA_PORT = os.environ['PGPORT']
    DATA_PROD1_URL = ('postgresql://' + DATA_USERNAME + ':' + DATA_PASSWORD +
                      '@' + DATA_HOSTNAME + ':' + DATA_PORT + '/' + db_name)
    return create_engine(DATA_PROD1_URL)
