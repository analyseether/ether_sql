import logging
import settings
import sqlalchemy
import sys

from web3 import (
    Web3,
    IPCProvider,
    HTTPProvider,
)
from ether_sql.models import base

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


def setup_db_engine(user, password, db, host='localhost', port=5432):
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

    # Create an engine that stores data in the PostgreSQL
    engine = sqlalchemy.create_engine(url, client_encoding='utf8')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    base.metadata.bind = engine

    logger.info('Connected to the db {}'.format(db))

    return engine


def setup_node_session(node_type, node_url):
    """
    Connects to appropriate node using values specified in settings.py

    :param str node_type: Type of node, available options 'Parity', 'Geth' and 'Infura'
    :param str node_url: url of connection if an HTTP connection
    """
    PARSE_TRACE = settings.PARSE_TRACE
    if node_type == 'Parity':
        w3 = Web3(IPCProvider())

        # checking if trace tables should be parsed
        if PARSE_TRACE:
            try:
                trace = w3.parity.traceBlock('latest')
            except ValueError:
                trace = None
                raise ValueError('Trace configuration not active')
            finally:
                if trace is None:
                    PARSE_TRACE = False
                    logger.warning('Tracing not active switching off parsing trace tables')
                else:
                    # if trace module is available extend the time of connection
                    w3 = Web3(IPCProvider(timeout=60))
    elif node_type == 'Geth':
        w3 = Web3(IPCProvider())
    elif node_type == 'Infura':
        w3 = Web3(HTTPProvider(settings.NODE_URL))
    else:
        raise ValueError('Node {} not supported'.format(node_type))

    if w3.isConnected:
        logger.info('Connected to {} node'.format(node_type))
    else:
        logger.error('{} node failed connecting to network'.format(node_type))

    return w3, PARSE_TRACE


setup_logging()

db_engine = setup_db_engine(user=settings.SQLALCHEMY_USER,
                            password=settings.SQLALCHEMY_PASSWORD,
                            db=settings.SQLALCHEMY_DB)

w3, PARSE_TRACE = setup_node_session(node_type=settings.NODE_TYPE,
                                               node_url=settings.NODE_URL)
