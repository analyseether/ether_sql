import os
import inspect
import sys

# Task queue settings
RABBIT_MQ_URL = 'amqp://myuser:mypassword@localhost:5672/myvhost'
CELERY_BROKER = RABBIT_MQ_URL
CELERY_BACKEND = 'rpc://'
CELERYD_TASK_SOFT_TIME_LIMIT = 60
CELERYD_TASK_TIME_LIMIT = 120
CELERYD_LOG_FORMAT = '[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] %(message)s'
CELERYD_TASK_LOG_FORMAT = '[%(asctime)s][PID:%(process)d][%(levelname)s][%(processName)s] task_name=%(task_name)s taks_id=%(task_id)s %(message)s'


class DefaultSettings():
    # SQLALCHEMY settings
    SQLALCHEMY_USER = os.environ.get("USER")
    # password that is set when creating psql user
    SQLALCHEMY_PASSWORD = 'develop'
    SQLALCHEMY_DB = 'ether_sql'
    SQLALCHEMY_HOST = 'localhost'
    SQLALCHEMY_PORT = 5432

    # Logging settings
    LOG_STDOUT = "TRUE"
    LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
    LOG_LEVEL = "INFO"

    # Node settings
    # Available options 'Geth', 'Parity', 'Infura'
    NODE_TYPE = "Infura"
    NODE_URL = 'https://mainnet.infura.io/'
    TIMEOUT = 10
    # Tables to parse
    # Use this option to parse traces, needs parity with cli --tracing=on
    PARSE_TRACE = False
    PARSE_STATE_DIFF = False
    NEW_BLOCKS = False
    BLOCK_LAG = 100
    FILTER_TIME = 30

class PersonalInfuraSettings(DefaultSettings):
    NODE_TYPE = "Infura"
    NODE_API_TOKEN = ""  # your infura api_token
    NODE_URL = 'https://mainnet.infura.io/{}'.format(NODE_API_TOKEN)


class PersonalParitySettings(DefaultSettings):
    NODE_TYPE = "Parity"
    PARSE_TRACE = True
    PARSE_STATE_DIFF = True
    TIMEOUT = 60


class PersonalGethSettings(DefaultSettings):
    NODE_TYPE = "Geth"


class TestSettings(DefaultSettings):
    # SQLALCHEMY settings
    SQLALCHEMY_PASSWORD = 'develop'
    SQLALCHEMY_DB = 'ether_sql_tests'
    NEW_BLOCKS = False
    # Logging settings
    LOG_LEVEL = "DEBUG"
    BLOCK_LAG = 1


class ParityTestSettings(TestSettings):

    # Node settings
    # Available options 'Geth', 'Parity', 'Infura'
    NODE_TYPE = "Parity"
    # Tables to parse
    # Use this option to parse traces, needs parity with cli --tracing=on
    PARSE_TRACE = True
    PARSE_STATE_DIFF = True
    TIMEOUT = 60
    NEW_BLOCKS = True
    BLOCK_LAG = 1
    FILTER_TIME = 1

def get_setting_names():
    setting_names = []
    settings_module = sys.modules[__name__]
    for name, obj in inspect.getmembers(settings_module):
        if inspect.isclass(obj):
            setting_names.append(name)
    return setting_names
