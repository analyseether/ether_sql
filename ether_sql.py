#!/usr/bin/env python
"""
CLI to manage ether_sql.
"""
import click


@click.group()
def cli():
    "CLI group for ether_sql"


@cli.command()
def check_settings():
    """Show the settings as ether_sql sees them (useful for debugging)."""
    import settings
    for name, item in settings.all_settings().iteritems():
        print("{} = {}".format(name, item))


@cli.command()
def create_tables():
    """Create the database tables."""
    from ether_sql.models import db
    from ether_sql import session

    db.metadata.create_all(session)
    click.echo('Created the tables')


@cli.command()
def drop_tables():
    """Drop the database tables."""
    from ether_sql.models import db
    from ether_sql import session

    db.metadata.drop_all(session)
    click.echo('Dropped the tables')


if __name__ == '__main__':
    cli()
