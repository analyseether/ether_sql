import os

# SQLALCHEMY settings
SQLALCHEMY_USER = os.environ.get("USER")
SQLALCHEMY_PASSWORD = 'develop'  # password that is set when creating psql user
SQLALCHEMY_DB = 'ether-sql'

# Logging settings
LOG_STDOUT = "TRUE"
LOG_FORMAT = "[%(asctime)s][PID:%(process)d][%(levelname)s][%(name)s] %(message)s"
LOG_LEVEL = "DEBUG"
