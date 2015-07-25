"""Example CLI provided by module."""

import click
from flask import current_app
from flask_cli import with_appcontext


@click.group()
def cli():
    """Module CLI."""


@cli.command()
def testsimple():
    """Command without application context."""
    click.echo("Test")


@cli.command()
@with_appcontext
def testapp():
    """Command with application context."""
    click.echo(current_app.name)
