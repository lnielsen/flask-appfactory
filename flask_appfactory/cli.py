# -*- coding: utf-8 -*-

"""Command line interface for ArchivalStorage."""

from __future__ import absolute_import, unicode_literals, print_function

from flask.ext.script import Manager
from flask.ext.registry import ModuleAutoDiscoveryRegistry


import click
from flask.cli import FlaskGroup


def create_cli(create_app):
    """Create CLI for Flask Application."""
    def cli_create_app(dummy_info):
        return create_app()

    @click.group(cls=FlaskGroup, create_app=cli_create_app)
    def cli(**params):
        """Management script for the Archival Storage application."""

    return cli
