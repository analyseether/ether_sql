import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Manages the ether node (query the node)."""

@cli.command()
def eth_blockNumber():
    """
    Gives the most recent block number in the ether node
    """
    from ether_sql import node_session
    click.echo("Block number: {}".format(node_session.eth_blockNumber()))
