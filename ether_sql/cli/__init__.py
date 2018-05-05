import click
from ether_sql.cli import database


@click.group()
def cli():
    """CLI script for ether_sql"""


cli.add_command(database.cli, "database")


@cli.command()
def check_settings():
    """Show the settings as ether_sql sees them (useful for debugging)."""
    import settings
    for name, item in settings.all_settings().iteritems():
        print("{} = {}".format(name, item))
