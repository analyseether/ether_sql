import logging
import settings
import sqlalchemy
import sys
from ethjsonrpc import EthJsonRpc, ParityEthJsonRpc, InfuraEthJsonRpc

logger = logging.getLogger(__name__)


def setup_logging():
    """
    Add logging format to logger used for debugging and info
    """

    handler = logging.StreamHandler(sys.stdout if settings.LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG_LEVEL)


def setup_db_session(user, password, db, host='localhost', port=5432):
    """
    Connects to the psql database given its parameters and returns the
    connection session

    We connect with the help of the PostgreSQL URL
    example url--> postgresql://federer:grandestslam@localhost:5432/tennis
    inspired from: https://suhas.org/sqlalchemy-tutorial/

    :param user: user who owns the database
    :param password: password if needed to unlock this database
    :param host: host port to connect to this database
    :param db: name of the database

    :return: The connection to the database
    """

    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

    # The return value of create_engine() is our connection object
    session = sqlalchemy.create_engine(url, client_encoding='utf8')

    logging.info('Connected to the db {}'.format(db))

    return session


def setup_node_session(node_type, host='localhost', port=8545, api_token=''):
    """
    Connects to appropriate node using values specified in settings.py

    :param str node_type: Type of node, available options 'Parity', 'Geth' and 'Infura'
    :param str host: Name of host
    :param int port: Port number of the connection
    :param str api_token: Api token if needed
    """

    if node_type == 'Parity':
        node = ParityEthJsonRpc(host=host, port=port)
    elif node_type == 'Geth':
        node = EthJsonRpc(host=host, port=port)
    elif node_type == 'Infura':
        network = host.split('.')[0]  # getting the network name
        node = InfuraEthJsonRpc(network=network, infura_token=api_token)
    else:
        raise ValueError('Node {} not supported'.format(node_type))

    logging.info('Connected to {} node'.format(node_type))

    return node


setup_logging()

db_session = setup_db_session(user=settings.SQLALCHEMY_USER,
                              password=settings.SQLALCHEMY_PASSWORD,
                              db=settings.SQLALCHEMY_DB)

node_session = setup_node_session(node_type=settings.NODE_TYPE,
                                  host=settings.NODE_HOST,
                                  port=settings.NODE_PORT,
                                  api_token=settings.NODE_API_TOKEN)
