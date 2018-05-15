import click
from ether_sql.cli import sql, ether
from sqlalchemy.orm import sessionmaker
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """CLI script for ether_sql"""


cli.add_command(sql.cli, "sql")
cli.add_command(ether.cli, "ether")


@cli.command()
def check_settings():
    """Show the settings as ether_sql sees them (useful for debugging)."""
    import settings
    for name, item in settings.all_settings().iteritems():
        click.echo("{} = {}".format(name, item))


@cli.command()
@click.option('--sql_block_number', default=None, help='block number in sql')
@click.option('--node_block_number', default=None, help='block number in node')
def scrape_data(sql_block_number, node_block_number):
    """
    Pushes the data between sql_block_number and node_block_number in the database
    """
    from sqlalchemy import func

    from ether_sql import node_session, db_engine
    from ether_sql.scrapper import scrape_blocks
    from ether_sql.models import Blocks

    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    DBSession = sessionmaker(bind=db_engine)
    db_session = DBSession()

    if node_block_number is None:
        node_block_number = node_session.eth_blockNumber()
    if sql_block_number is None:
        sql_block_number = db_session.query(func.max(Blocks.block_number)).scalar()
        if sql_block_number is None:
            sql_block_number = 0

    # casting numbers to integers
    sql_block_number = int(sql_block_number)
    node_block_number = int(node_block_number)

    if sql_block_number == node_block_number:
        logger.warning('Start block: {}; end block: {}; no data scrapped'
                       .format(sql_block_number, node_block_number))
    scrape_blocks(session=db_session,
                  sql_block_number=sql_block_number,
                  node_block_number=node_block_number)
