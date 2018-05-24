import logging
import sqlalchemy
import sys
from web3 import (
    Web3,
    IPCProvider,
    HTTPProvider,
)
from ether_sql.models import base
from ether_sql.settings import (
    DefaultSettings,
    TestSettings,
    ParityTestSettings,
    PersonalInfuraSettings,
    SETTINGS_MAP,
)
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class Session():
    def __init__(self, settings=None):

        if settings is None:
            self.setting_name = 'DefaultSettings'
        else:
            self.setting_name = settings

        try:
            self.settings = SETTINGS_MAP[self.setting_name]
        except KeyError:
            raise ValueError('Invalid setting, choose one of these {}'
                             .format([key for key in SETTINGS_MAP.keys()]))

        self.db_engine = setup_db_engine(settings=self.settings)

        DBSession = sessionmaker(bind=self.db_engine)
        self.db_session = DBSession()

        self.w3 = setup_node_session(settings=self.settings)

        setup_logging(settings=self.settings)


def setup_logging(settings):
    """
    Add logging format to logger used for debugging and info
    """

    handler = logging.StreamHandler(sys.stdout if settings.LOG_STDOUT else sys.stderr)
    formatter = logging.Formatter(settings.LOG_FORMAT)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(settings.LOG_LEVEL)


def setup_db_engine(settings):
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
    url = url.format(settings.SQLALCHEMY_USER,
                     settings.SQLALCHEMY_PASSWORD,
                     settings.SQLALCHEMY_HOST,
                     settings.SQLALCHEMY_PORT,
                     settings.SQLALCHEMY_DB)

    # Create an engine that stores data in the PostgreSQL
    engine = sqlalchemy.create_engine(url, client_encoding='utf8')
    base.metadata.bind = engine
    logger.info('Connected to the db {}'.format(settings.SQLALCHEMY_DB))

    return engine


def setup_node_session(settings):
    """
    Connects to appropriate node using values specified in settings.py

    :param str node_type: Type of node, 'Parity', 'Geth' or 'Infura'
    :param str node_url: url of connection if an HTTP connection
    """
    if settings.NODE_TYPE == 'Parity':
        # checking if trace tables should be parsed
        if settings.PARSE_TRACE:
            w3 = Web3(IPCProvider(timeout=60))
        else:
            w3 = Web3(IPCProvider())

    elif settings.NODE_TYPE == 'Geth':
        w3 = Web3(IPCProvider())
    elif settings.NODE_TYPE == 'Infura':
        w3 = Web3(HTTPProvider(settings.NODE_URL))
    else:
        raise ValueError('Node {} not supported'.format(settings.NODE_TYPE))

    if w3.isConnected:
        logger.info('Connected to {} node'.format(settings.NODE_TYPE))
    else:
        logger.error('{} node failed connecting to network'.format(settings.NODE_TYPE))

    return w3
