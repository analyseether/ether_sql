import click
import logging
from ether_sql.globals import get_current_session

logger = logging.getLogger(__name__)


@click.group()
@click.pass_context
def ether(ctx):
    """Manages the ether node (query the node)."""


@ether.command()
@click.pass_context
def blockNumber(ctx):
    """
    Gives the most recent block number in the ether node
    """
    current_session = get_current_session()
    click.echo(current_session.w3.eth.blockNumber)
