import click
import logging
from ether_sql.tasks.worker import app


logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def celery(ctx):
    """Manages the celery workers (start and stop celery)."""


@celery.command(context_settings=dict(ignore_unknown_options=True,
                                      allow_extra_args=True,))
@click.pass_context
@click.option('-l', '--loglevel', default='info',
              help='Specifies the log level for the celery workers')
@click.option('-c', '--concurrency', default=4,
              help='Number of parallel workers')
def start(ctx, loglevel, concurrency):
    """
    Starts the celery workers, also allows for passing celery specific arguements.
    """
    click.echo(ctx.args)
    list_argument = ['celery', 'worker', '-l', loglevel,
                     '-c{}'.format(concurrency)]
    list_argument.extend(ctx.args)
    click.echo(list_argument)
    app.start(argv=list_argument)


@celery.command()
@click.pass_context
def shutdown(ctx):
    """
    Stops the celery workers
    """
    app.start(argv=['celery', 'control', 'shutdown'])
