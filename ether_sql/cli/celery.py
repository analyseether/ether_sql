import click
import logging


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def celery(ctx):
    """Manages the celery workers (start and stop celery)."""


@celery.command()
@click.pass_context
@click.option('-l', '--loglevel', default='info',
              help='Specifies the log level for the celery workers')
@click.option('-c', '--concurrency', default=4,
              help='Number of parallel workers')
def start(ctx, loglevel, concurrency):
    """
    Starts the celery workers
    """
    from ether_sql.tasks.worker import app
    app.start(argv=['celery', 'worker', '-l', loglevel, '-c{}'.format(concurrency)])
