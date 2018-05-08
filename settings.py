import os


def all_settings():
    """Return list of all settings"""
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") and not isinstance(item, ModuleType):
            settings[name] = item

    return settings


# SQLALCHEMY settings
SQLALCHEMY_USER = os.environ.get("USER")
SQLALCHEMY_PASSWORD = 'develop'  # password that is set when creating psql user
SQLALCHEMY_DB = 'ether_sql'

# Logging settings
LOG_STDOUT = "TRUE"
LOG_FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
LOG_LEVEL = "DEBUG"

# Node settings
NODE_TYPE = "Infura"  # Available options 'Geth', 'Parity', 'Infura'
NODE_API_TOKEN = ""
NODE_HOST = 'mainnet.infura.io'
NODE_PORT = 8545
