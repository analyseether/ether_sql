import click
import logging

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def cli(ctx):
    """Manages the ether node (query the node)."""


@cli.command()
@click.pass_context
def blockNumber(ctx):
    """
    Gives the most recent block number in the ether node
    """
    session = ctx.obj['session']
    click.echo(session.w3.eth.blockNumber)
