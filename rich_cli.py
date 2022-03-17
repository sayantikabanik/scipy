import click
import os
from rich_click import RichCommand, RichGroup


@click.group(cls=RichGroup)
def cli():
    """
    Scipy tasks
    """
    click.echo(f"Scipy build successful")


@cli.command(cls=RichCommand)
def doc_build():
    """Initializing document build"""
    click.echo(f"Scipy doc build successful")


if __name__ == "__main__":
    cli()
