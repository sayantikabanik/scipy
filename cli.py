"""
Info: Run tests, builds and other tasks using, typer and system package
-------
    cmd options:
        $ python cli.py --help
        $ python cli.py bench <flag>
        $ python cli.py test <flag> <module>
        $ python cli.py build
        $ python cli.py doc-build
"""
# TODO: Add release tasks

from typing import Optional
import typer
import os

app = typer.Typer()


@app.command()
def build():
    """
    Run Scipy build
    """
    os.system("python dev.py --build-only")


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def bench(ctx: typer.Context):
    """
    Run benchmark options
    """
    for extra_arg in ctx.args:
        os.system(f"python dev.py --bench {extra_arg} integrate.SolveBVP")


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def test(ctx: typer.Context):
    """
    Run test for a given module
    """
    _arg = ""
    for extra_arg in ctx.args:
        _arg += extra_arg + " "
    os.system(f"python dev.py --no-build {_arg}")


@app.command()
def doc_build():
    """
    Run document build tasks
    """
    build()
    os.system("python dev.py --doc")


if __name__ == '__main__':
    app()
