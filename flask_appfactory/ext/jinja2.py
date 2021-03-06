# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Jinja2 loader and extensions initialization."""

from __future__ import absolute_import, unicode_literals, print_function

from distutils.version import LooseVersion
from flask.templating import DispatchingJinjaLoader
from flask import __version__ as flask_version
from jinja2 import ChoiceLoader

# Flask 1.0 changes return value of _iter_loaders so for compatibility with
# both Flask 0.10 and 1.0 we here check the version.
# See Flask commit bafc13981002dee4610234c7c97ac176766181c1
IS_FLASK_1_0 = LooseVersion(flask_version) >= LooseVersion("0.11-dev")

try:
    # Deprecated in Flask commit 817b72d484d353800d907b3580c899314bf7f3c6
    from flask.templating import blueprint_is_module
except ImportError:
    def blueprint_is_module(blueprint):
        """Dummy function for Flask 1.0."""
        return False


class OrderAwareDispatchingJinjaLoader(DispatchingJinjaLoader):

    """Order aware dispatching Jinja loader.

    Customization of default Flask Jinja2 template loader. By default the
    Flask Jinja2 template loader is not aware of the order of Blueprints as
    defined by the PACKAGES configuration variable.
    """

    def _iter_loaders(self, template):
        for blueprint in self.app.extensions['registry']['blueprints']:
            if blueprint_is_module(blueprint):
                continue
            loader = blueprint.jinja_loader
            if loader is not None:
                if IS_FLASK_1_0:
                    yield blueprint, loader
                else:
                    yield loader, template


def setup_app(app):
    """Initialize Jinja2 loader and extensions."""
    # Customize Jinja loader.

    jinja_loader = ChoiceLoader([
        OrderAwareDispatchingJinjaLoader(app),
        app.jinja_loader,
    ])
    app.jinja_loader = jinja_loader

    # Load Jinja extensions
    for ext in app.config.get('JINJA2_EXTENSIONS', []):
        app.jinja_env.add_extension(ext)
