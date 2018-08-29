import logging
import os
import sqlalchemy
import sys
import argparse
from alembic.config import Config
from web3 import (
    Web3,
    IPCProvider,
    HTTPProvider,
)
from contextlib import contextmanager
from ether_sql.models import base
import ether_sql.settings as settings
from sqlalchemy.orm import sessionmaker
logger = logging.getLogger(__name__)


class Session():

    def __init__(self, setting_name=None):

        if setting_name is None:
            self.setting_name = 'DefaultSettings'
        else:
            self.setting_name = setting_name

        try:
            self.settings = getattr(settings, self.setting_name)
        except KeyError:
            raise ValueError('The desired setting does not exist')

        setup_logging(settings=self.settings)
        logger.debug(self.settings.LOG_LEVEL)

        self.db_engine, self.url = setup_db_engine(settings=self.settings)

        self.w3 = setup_node_session(settings=self.settings)

        if self.settings.NEW_BLOCKS:
            print("Adding block filters")
            self.setup_filters()

    @contextmanager
    def db_session_scope(self):
        DBSession = sessionmaker(bind=self.db_engine)
        self.db_session = DBSession()

        try:
            yield self.db_session
            # logger.debug("New data {}".format(self.db_session.new))
            # logger.debug("Updated data {}".format(self.db_session.dirty))
            self.db_session.commit()
        except Exception as e:
            self.db_session.rollback()
            raise e
        finally:
            self.db_session.close()

    def setup_filters(self):
        self.block_filter = self.w3.eth.filter('latest')

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
    engine = sqlalchemy.create_engine(url, client_encoding='utf8',
                isolation_level="AUTOCOMMIT")

    base.metadata.bind = engine
    logger.info('Connected to the db {}'.format(settings.SQLALCHEMY_DB))

    return engine, url


def setup_node_session(settings):
    """
    Connects to appropriate node using values specified in settings.py

    :param str node_type: Type of node, 'Parity', 'Geth' or 'Infura'
    :param str node_url: url of connection if an HTTP connection
    """
    if settings.NODE_TYPE == 'Parity':
        # checking if trace tables should be parsed
        w3 = Web3(IPCProvider(timeout=settings.TIMEOUT))

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


def setup_alembic_config(url):
    "setting up generic config for alembic migrations"
    directory = 'ether_sql/migrations'
    config = Config(os.path.join(directory, 'alembic.ini'))
    config.set_main_option('script_location', directory)
    config.cmd_opts = argparse.Namespace()   # arguments stub
    x_arg = 'url=' + url
    if not hasattr(config.cmd_opts, 'x'):
        if x_arg is not None:
            setattr(config.cmd_opts, 'x', [])
            if isinstance(x_arg, list) or isinstance(x_arg, tuple):
                for x in x_arg:
                    config.cmd_opts.x.append(x)
            else:
                config.cmd_opts.x.append(x_arg)
        else:
            setattr(config.cmd_opts, 'x', None)
    return config
