import click
import logging
from alembic import command
from ether_sql.session import setup_alembic_config
from ether_sql.globals import get_current_session
from ether_sql.models import Blocks

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def sql(ctx):
    """Manages the sql (create/drop/query tables)."""


@sql.command()
@click.pass_context
def create_tables(ctx):
    """
    This is a depreceated function. Alias for `ether_sql sql upgrade_tables`
    """
    ctx.invoke(upgrade_tables)


@sql.command()
@click.pass_context
def drop_tables(ctx):
    """ Alias for 'alembic downgrade base'.
    Downgrade to no database tables
    """
    current_session = get_current_session()
    command.downgrade(setup_alembic_config(url=current_session.url),
                      revision='base', sql=False, tag=None)


@sql.command()
@click.pass_context
def blockNumber(ctx):
    """ Gives the current highest block in database"""
    click.echo(Blocks.get_max_block_number())


@sql.command()
@click.option('-m', '--message', default=None,
              help='Write a message specifying what changed')
@click.pass_context
def migrate(ctx, message):
    """ Alias for 'alembic revision --autogenerate'
    Run this command after changing sql tables
    """
    current_session = get_current_session()
    if message is None:
        click.echo(ctx.get_help())
    else:
        command.revision(setup_alembic_config(url=current_session.url),
                         message=message, autogenerate=True, sql=None)


@sql.command()
@click.pass_context
def upgrade_tables(ctx):
    """ Alias for 'alembic upgrade head'.
    Upgrade to latest model version
    """
    current_session = get_current_session()
    command.upgrade(setup_alembic_config(url=current_session.url),
                    revision='head', sql=False, tag=None)


@sql.command()
@click.pass_context
@click.option('--directory', default='.',
              help='Directory where the csv should be exported')
@click.option('--mode', default='single',
              help='Choose single is using same thread or parallel if \
              using multiple threads')
def export_to_csv(ctx, directory, mode):
    """
    Export the data pushed into sql as csv
    """
    from ether_sql.tasks.export import export_to_csv
    if mode == 'parallel':
        export_to_csv.delay(directory=directory)
    elif mode == 'single':
        export_to_csv(directory=directory)
    else:
        raise ValueError('The mode: {} is not recognized'.format(mode))
    click.echo("Exported all csv's")
