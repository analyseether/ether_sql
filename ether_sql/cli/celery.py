import click
import logging


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def celery(ctx):
    """Manages the celery workers (start and stop celery)."""


@celery.command()
@click.pass_context
def start(ctx):
    """
    Starts the celery workers
    """
    from ether_sql.tasks.worker import celery
    celery.start(argv=['celery', 'worker', '-l', 'info', '-c2'])
