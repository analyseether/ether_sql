import click
import logging
from ether_sql.models import base

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def cli(ctx):
    """Manages the sql (create/drop/query tables)."""


@cli.command()
@click.pass_context
def create_tables(ctx):
    """Create the database tables."""
    session = ctx.obj['session']
    logger.debug("{}".format(session.db_engine.url))
    base.metadata.create_all(session.db_engine)
    logger.info('Created the tables')


@cli.command()
@click.pass_context
def drop_tables(ctx):
    """Drop the database tables."""
    session = ctx.obj['session']
    logger.debug("{}".format(session.db_engine.url))
    base.metadata.drop_all(session.db_engine)
    logger.info('Dropped the tables')


@cli.command()
def sql_blockNumber():
    """ Gives the current highest block in database"""
    from ether_sql import db_engine
    from ether_sql.models import Blocks
    from sqlalchemy import func
    from sqlalchemy.orm import sessionmaker

    DBSession = sessionmaker(bind=db_engine)
    db_session = DBSession()

    max_block_number = db_session.query(func.max(Blocks.block_number)).scalar()
    click.echo("{}".format(max_block_number))
