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
    for name, item in list(settings.all_settings().items()):
        click.echo("{} = {}".format(name, item))


@cli.command()
@click.option('--start_block_number', default=None, help='start block number')
@click.option('--end_block_number', default=None, help='end block number')
def scrape_block_range(start_block_number, end_block_number):
    """
    Pushes the data between start_block_number and end_block_number in the database
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

    if start_block_number is None:
        end_block_number = node_session.eth_blockNumber()
    if end_block_number is None:
        start_block_number = db_session.query(func.max(Blocks.block_number)).scalar()
        if start_block_number is None:
            start_block_number = 0

    # casting numbers to integers
    start_block_number = int(start_block_number)
    end_block_number = int(end_block_number)

    if start_block_number == end_block_number:
        logger.warning('Start block: {}; end block: {}; no data scrapped'
                       .format(start_block_number, end_block_number))
    scrape_blocks(session=db_session,
                  start_block_number=start_block_number,
                  end_block_number=end_block_number)


@cli.command()
@click.option('--block_number', default=None, help='block number to add')
def scrape_block(block_number):
    """
    Pushes the data in block_number in the database
    """
    from ether_sql import db_engine
    from ether_sql.scrapper import add_block_number

    DBSession = sessionmaker(bind=db_engine)
    session = DBSession()

    if block_number is not None:
        block_number = int(block_number)
        session = add_block_number(block_number=block_number, session=session)
        session.commit()
    else:
        raise ValueError('Please provide a value of --block_number')
