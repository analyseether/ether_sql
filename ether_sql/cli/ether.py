import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Manages the ether node (query the node)."""
