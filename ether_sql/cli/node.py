import click
import logging

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """Manages the node (query the node)."""
