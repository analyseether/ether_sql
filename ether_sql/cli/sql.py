import click
import logging
from alembic import command
from sqlalchemy import func
from ether_sql.session import setup_alembic_config
from ether_sql.globals import get_current_session

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
    current_session = get_current_session()
    current_session.setup_db_session()

    max_block_number = current_session.db_session.query(
        func.max(Blocks.block_number)).scalar()
    current_session.db_session.close()

    click.echo(max_block_number)


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
    from ether_sql.tasks.worker import celery_is_running, redis_is_running
    if mode == 'parallel':
        if celery_is_running() and redis_is_running():
            logger.info('Celery and Redis are running, using multiple threads')
            export_to_csv.delay(directory=directory)
        else:
            raise AttributeError('Switch on celery and redis to use parallel mode')
    elif mode == 'single':
        export_to_csv(directory=directory)
    else:
        raise ValueError('The mode: {} is not recognized'.format(mode))
    click.echo("Exported all csv's")
