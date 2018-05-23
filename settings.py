import os


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
    # Tables to parse
    # Use this option to parse traces, needs parity with cli --tracing=on
    PARSE_TRACE = False


class PersonalInfuraSettings(DefaultSettings):
    NODE_TYPE = "Infura"
    NODE_API_TOKEN = ""  # your infura api_token
    NODE_URL = 'https://mainnet.infura.io/{}'.format(NODE_API_TOKEN)


class PersonalParitySettings(DefaultSettings):
    NODE_TYPE = "Parity"
    PARSE_TRACE = True


class TestSettings(DefaultSettings):
    # SQLALCHEMY settings
    SQLALCHEMY_DB = 'ether_sql_tests'

    # Logging settings
    LOG_LEVEL = "DEBUG"


class ParityTestSettings(TestSettings):

    # Node settings
    # Available options 'Geth', 'Parity', 'Infura'
    NODE_TYPE = "Parity"

    # Tables to parse
    # Use this option to parse traces, needs parity with cli --tracing=on
    PARSE_TRACE = True


SETTINGS_MAP = {'DefaultSettings': DefaultSettings,
                'TestSettings': TestSettings,
                'ParityTestSettings': ParityTestSettings,
                'PersonalInfuraSettings': PersonalInfuraSettings,
                'PersonalParitySettings': PersonalParitySettings,}
