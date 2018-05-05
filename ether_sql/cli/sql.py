import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Manages the sql (create/drop/query tables)."""


@cli.command()
def create_tables():
    """Create the database tables."""
    from ether_sql.models import db
    from ether_sql import session

    db.metadata.create_all(session)
    logger.info('Created the tables')


@cli.command()
def drop_tables():
    """Drop the database tables."""
    from ether_sql.models import db
    from ether_sql import session

    db.metadata.drop_all(session)
    logger.info('Dropped the tables')
