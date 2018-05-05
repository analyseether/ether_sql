import click


@click.group()
def cli():
    """Manage the database (create/drop tables)."""


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
