from threading import local
import logging

_local = local()

logger = logging.getLogger(__name__)


def get_current_session(silent=False):
    """
    Returns the current session, this can be used as a way to
    access the current session object from anywhere.

    :param silent: is set to `True` the return value is `None` if no context
                   is available.  The default behavior is to raise a
                   :exc:`RuntimeError`.
    """
    try:
        return _local.ether_sql_session
    except (AttributeError, IndexError):
        if not silent:
            raise RuntimeError('There is no active ether_sql session.')


def push_session(session):
    """Pushes the session to local thread."""
    logger.info('Pushing the session {} in local thread'.
                format(session.setting_name))
    _local.ether_sql_session = session
