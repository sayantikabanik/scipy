import click
import os
from rich_click import RichCommand, RichGroup


@click.group(cls=RichGroup)
def cli():
    """
    Scipy tasks
    """
    click.echo(f"Initiating Scipy build")


@cli.command(cls=RichCommand)
def doc_build():
    """Initializing document build"""
    click.echo(f"Initiating Scipy doc build")


if __name__ == "__main__":
    cli()
