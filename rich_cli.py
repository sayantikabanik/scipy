import click
import os
from rich_click import RichCommand, RichGroup


"""
group 01 and subcommands
"""


@click.group(cls=RichGroup)
def cli():
    """
    Scipy tasks
    """
    click.echo(f"Scipy task successful")


@cli.command(cls=RichCommand)
def build():
    """Initializing build tasks"""
    click.echo(f"Scipy build successful")


@cli.command(cls=RichCommand)
def doc_build():
    """Initializing document build"""
    click.echo(f"Scipy doc build successful")


"""
group 02 and subcommands
"""


@click.group(cls=RichGroup)
def release_cli():
    """
    Release task
    """
    click.echo(f"Scipy release task successful")


@release_cli.command(cls=RichCommand)
def release_notes():
    """Initializing scipy log"""
    click.echo(f"Scipy log generation successful")


@release_cli.command(cls=RichCommand)
def release_authors():
    """Initializing scipy author list generation"""
    click.echo(f"Scipy author list generation successful")


if __name__ == "__main__":
    cli()
    release_cli()
