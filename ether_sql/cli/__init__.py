import click
from ether_sql.cli import sql, ether


@click.group()
def cli():
    """CLI script for ether_sql"""


cli.add_command(sql.cli, "sql")
cli.add_command(ether.cli, "ether")


@cli.command()
def check_settings():
    """Show the settings as ether_sql sees them (useful for debugging)."""
    import settings
    for name, item in settings.all_settings().iteritems():
        click.echo("{} = {}".format(name, item))
