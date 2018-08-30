import click
import logging
from ether_sql.cli import sql, ether, celery
from ether_sql.session import Session
from ether_sql.tasks.scrapper import scrape_blocks, add_block_number
from ether_sql.models import Blocks
from ether_sql.globals import push_session, get_current_session
from ether_sql.settings import get_setting_names
logger = logging.getLogger(__name__)

setting_names = get_setting_names()

@click.group()
@click.option('--settings', default='DefaultSettings',
              help='Settings to run ether_sql, choose from ' + ', '.join(setting_names)
              , show_default=True, type=click.Choice(setting_names), metavar="")
@click.pass_context
def cli(ctx, settings):
    """:code:`ether_sql` is the most basic CLI group with 4 subsequent
    commands."""
    current_session = Session(setting_name=settings)
    push_session(current_session)


cli.add_command(sql.sql, "sql")
cli.add_command(ether.ether, "ether")
cli.add_command(celery.celery, "celery")


@cli.command()
@click.option('--start_block_number', default=None, help='start block number')
@click.option('--end_block_number', default=None, help='end block number')
@click.option('--mode', default='single',
              help='Choose single is using same thread or parallel if \
              using multiple threads')
@click.option('--fill_gaps/--no-fill_gaps', default=True)
@click.pass_context
def scrape_block_range(ctx, start_block_number, end_block_number, mode, fill_gaps):
    """
    Pushes the data between start_block_number and end_block_number in the
    database. If no values are provided, the start_block_number is the last
    block_number+1 in sql and end_block_number is the current block_number in
    node. Also checks for missing blocks and adds them to the list of required
    block numbers

    :param int start_block_number: starting block number of scraping
    :param int end_block_number: end block number of scraping
    :param str mode: Mode of data sync 'parallel' or single
    :param bool fill_gaps: If switched on instructs to also fill missing blocks
    """

    current_session = get_current_session()
    with current_session.db_session_scope():
        sql_block_number = Blocks.get_max_block_number()
    if end_block_number is None:
        end_block_number = current_session.w3.eth.blockNumber
        logger.debug(end_block_number)
    if start_block_number is None:
        if sql_block_number is None:
            start_block_number = 0
        elif sql_block_number == end_block_number:
            start_block_number = sql_block_number
        else:
            start_block_number = sql_block_number+1
    logger.debug(start_block_number)

    # casting numbers to integers
    if start_block_number == end_block_number:
        list_block_numbers = []
    else:
        start_block_number = int(start_block_number)
        end_block_number = int(end_block_number)
        list_block_numbers = list(range(start_block_number, end_block_number+1))

    if fill_gaps and start_block_number != 0:
        missing_blocks = Blocks.missing_blocks(sql_block_number)
        logger.debug(missing_blocks)
        logger.info('{} missing blocks detected'.format(len(missing_blocks)))
        for missing in missing_blocks:
            logger.debug(missing.block_number)
            list_block_numbers.append(missing.block_number)

    logger.debug(list_block_numbers)
    if len(list_block_numbers) == 0:
        logger.warning('No blocks pushed in database')
    if mode == 'parallel':
        scrape_blocks(list_block_numbers=list_block_numbers,
                      mode=mode)
    elif mode == 'single':
        scrape_blocks(list_block_numbers=list_block_numbers,
                      mode=mode)
    else:
        raise ValueError('The mode: {} is not recognized'.format(mode))


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
