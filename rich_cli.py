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


@click.argument("log_start", type=str, required=True)
@click.argument("log_end", type=str, required=True)
@release_cli.command(cls=RichCommand)
def release_notes(log_start, log_end):
    """Initializing scipy log"""
    click.echo(f"Scipy log generation for {log_start} to {log_end}")


@release_cli.command(cls=RichCommand)
def release_authors():
    """Initializing scipy author list generation"""
    click.echo(f"Scipy author list generation successful")


if __name__ == "__main__":
    cli()
    release_cli()
