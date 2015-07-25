# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Command line interface factory."""

from __future__ import absolute_import, print_function, unicode_literals

import click
from flask_cli import FlaskGroup, ScriptInfo
from flask_registry import ModuleAutoDiscoveryRegistry

from .app import load_application


class CLIDiscoveryRegistry(ModuleAutoDiscoveryRegistry):

    """Discover CLI modules and register them on a command collection.

    Searches for a variable ``cli`` in a module ``cli`` in each package.

    :param cli_collection: A ``click.CommandCollection`` object.
    :param app: Flask application.
    """

    def __init__(self, cli_collection, app, **kwargs):
        """Initialize the registry."""
        self.cli_collection = cli_collection
        super(CLIDiscoveryRegistry, self).__init__('cli', app=app, **kwargs)

    def register(self, module):
        """Register modules with CLI variable."""
        module_cli = getattr(module, 'cli', None)
        if module_cli is not None and \
           isinstance(module_cli, click.BaseCommand):
            self.cli_collection.add_source(module_cli)
            super(CLIDiscoveryRegistry, self).register(module_cli)


class AppFactoryCollection(click.CommandCollection):

    """Special command collection for Flask-AppFactory.

    Ensures that a ``flask_cli.ScriptInfo`` object exists with a application
    factory function defined.

    :param create_cli_app: A application factory wrapper that takes a single
        argument (``flask_cli.ScriptInfo`` object). Function must return a
        Flask application.
    """

    def __init__(self, create_cli_app, *args, **kwargs):
        """Initialize command."""
        self.create_cli_app = create_cli_app
        super(AppFactoryCollection, self).__init__(*args, **kwargs)

    def main(self, *args, **kwargs):
        """Ensure the ``ScriptInfo`` object exists when called."""
        obj = kwargs.get('obj')
        if obj is None:
            obj = ScriptInfo(create_app=self.create_cli_app)
        kwargs['obj'] = obj
        return super(AppFactoryCollection, self).main(*args, **kwargs)


@click.group(cls=FlaskGroup)
def flask_cli(**params):
    """Base Flask commands."""


def clifactory(create_app, **config):
    """Create a click CLI application based on configuration.

    The CLI will install the default ``run`` and ``shell`` commands from Flask,
    and load commands from the list of modules defined in ``PACKAGES``. It will
    search in ``cli.py`` in each module for a variable ``cli``.

    The Flask application is not fully loaded unless the Flask app context is
    required.

    :param create_app: Flask application factory function.
    """
    # Create application object without loading the full application.
    app = create_app(load=False, **config)

    def create_cli_app(info):
        if not app.extensions['loaded']:
            load_application(app)
        return app

    # Create command collection
    cli = AppFactoryCollection(create_cli_app)
    cli.add_source(flask_cli)

    # Register CLI modules from packages.
    CLIDiscoveryRegistry(cli, app)

    return cli
