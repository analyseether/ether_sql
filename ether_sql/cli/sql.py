import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Manages the sql (create/drop/query tables)."""


@cli.command()
def create_tables():
    """Create the database tables."""
    from ether_sql.models import base
    from ether_sql import db_engine

    base.metadata.create_all(db_engine)
    logger.info('Created the tables')


@cli.command()
def drop_tables():
    """Drop the database tables."""
    from ether_sql.models import base
    from ether_sql import db_engine

    base.metadata.drop_all(db_engine)
    logger.info('Dropped the tables')


@cli.command()
def sql_blockNumber():
    """ Gives the current highest block in database"""
    from ether_sql import db_session
    from ether_sql.models import Blocks
    from sqlalchemy import func

    max_block_number = db_session.query(func.max(Blocks.block_number)).scalar()
    click.echo("{}".format(max_block_number))
