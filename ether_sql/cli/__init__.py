import click
import logging
from sqlalchemy import func

from ether_sql.cli import sql, ether, celery
from ether_sql.session import Session
from ether_sql.tasks.scrapper import scrape_blocks, add_block_number
from ether_sql.models import Blocks
from ether_sql.globals import push_session, get_current_session

logger = logging.getLogger(__name__)


@click.group()
@click.option('--settings', default='DefaultSettings',
              help='settings to run ether_sql')
@click.pass_context
def cli(ctx, settings):
    """:code:`ether_sql` is the most basic CLI group with 4 subsequent
    commands."""
    current_session = Session(settings=settings)
    push_session(current_session)


cli.add_command(sql.sql, "sql")
cli.add_command(ether.ether, "ether")
cli.add_command(celery.celery, "celery")


@cli.command()
@click.option('--start_block_number', default=None, help='start block number')
@click.option('--end_block_number', default=None, help='end block number')
@click.pass_context
def scrape_block_range(ctx, start_block_number, end_block_number):
    """
    Pushes the data between start_block_number and end_block_number in the
    database. If no values are provided, the start_block_number is the last
    block_number+1 in sql and end_block_number is the current block_number in
    node

    :param int start_block_number: starting block number of scraping
    :param int end_block_number: end block number of scraping
    """

    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    current_session = get_current_session()

    if end_block_number is None:
        end_block_number = current_session.w3.eth.blockNumber
        logger.debug(end_block_number)
    if start_block_number is None:
        sql_block_number = current_session.db_session.query(
                                func.max(Blocks.block_number)).scalar()
        if sql_block_number is None:
            start_block_number = 0
        else:
            start_block_number = sql_block_number+1
    logger.debug(start_block_number)

    # casting numbers to integers
    start_block_number = int(start_block_number)
    end_block_number = int(end_block_number)

    if start_block_number == end_block_number:
        logger.warning('Start block: {}; end block: {}; no data scrapped'
                       .format(start_block_number, end_block_number))
    scrape_blocks(start_block_number=start_block_number,
                  end_block_number=end_block_number)


@cli.command()
@click.option('--block_number', default=None, help='block number to add')
@click.pass_context
def scrape_block(ctx, block_number):
    """
    Pushes the data at block=block_number in the database
    """

    if block_number is not None:
        block_number = int(block_number)
        add_block_number(block_number=block_number)
    else:
        click.echo(ctx.get_help())
