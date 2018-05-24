import click
import logging
from sqlalchemy import func

from ether_sql.cli import sql, ether
from ether_sql.session import Session
from ether_sql.scrapper import scrape_blocks, add_block_number
from ether_sql.models import Blocks

logger = logging.getLogger(__name__)


@click.group()
@click.option('--settings', default='DefaultSettings',
              help='settings to run ether_sql')
@click.pass_context
def cli(ctx, settings):
    """CLI script for ether_sql"""
    if ctx.obj is None:
        ctx.obj = {}

    logger.debug('settings')
    ctx.obj['session'] = Session(settings=settings)


cli.add_command(sql.cli, "sql")
cli.add_command(ether.cli, "ether")


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
    """

    # A DBSession() instance establishes all conversations with the database
    # and represents a "staging zone" for all the objects loaded into the
    # database session object. Any change made against the objects in the
    session = ctx.obj['session']

    if end_block_number is None:
        end_block_number = session.w3.eth.blockNumber
        logger.debug(end_block_number)
    if start_block_number is None:
        sql_block_number = session.db_session.query(
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
    scrape_blocks(ether_sql_session=session,
                  start_block_number=start_block_number,
                  end_block_number=end_block_number)


@cli.command()
@click.option('--block_number', default=None, help='block number to add')
@click.pass_context
def scrape_block(ctx, block_number):
    """
    Pushes the data at block=block_number in the database
    """

    session = ctx.obj['session']
    if block_number is not None:
        block_number = int(block_number)
        session = add_block_number(block_number=block_number,
                                   ether_sql_session=session)
        logger.info("Commiting block: {} to sql".format(block_number))
        session.db_session.commit()
    else:
        click.echo(ctx.get_help())
