import click
import os
from rich_click import RichCommand, RichGroup


@click.group(cls=RichGroup)
def cli():
    """
    Scipy tasks
    """
    os.system("python dev.py --build-only")
    click.echo(f"Scipy build completed")


@cli.command(cls=RichCommand)
def doc_build():
    """Initializing document build"""
    os.system("python dev.py --doc")


if __name__ == "__main__":
    cli()
