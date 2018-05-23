import logging
import settings
from ether_sql.setup import (
    Session,
    setup_logging,
)

logger = logging.getLogger(__name__)

setup_logging(settings=settings.DefaultSettings)

session = Session()
