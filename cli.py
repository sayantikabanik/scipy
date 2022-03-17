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
    _args = ""
    for extra_arg in ctx.args:
        _args += extra_arg + " "
    os.system(f"python dev.py --no-build {_args}")


@app.command()
def doc_build():
    """
    Run document build tasks
    """
    build()
    os.system("python dev.py --doc")


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def release_notes(ctx: typer.Context):
    """
    Generating release notes
    """
    _args = ""
    for extra_arg in ctx.args:
        _args += "v" + extra_arg + " "
    os.system(f"python tools/write_release_and_log.py {_args}")


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def release_authors(ctx: typer.Context):
    """
    Generating contributor/author list
    """
    _args = ""
    for extra_arg in ctx.args:
        _args += "v" + extra_arg + ".."
    revision = _args.rstrip("..")
    os.system(f"python tools/authors.py {revision}")


if __name__ == '__main__':
    app()
