# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

"""Flask extension.


Flask-AppFactory is initialized like this:

>>> from flask import Flask
>>> from flask_appfactory import AppFactory

>>> app = Flask('myapp')
>>> ext = AppFactory(app=app)
"""

from __future__ import absolute_import

import logging
import os
import sys
import warnings

from flask import Flask
from flask.ext.registry import Registry, ExtensionRegistry, \
    PackageRegistry, ConfigurationRegistry, BlueprintAutoDiscoveryRegistry

from .version import __version__

__all__ = ('AppFactory', '__version__')


def configure_warnings():
    """Configure warnings by routing warnings to the logging system.

    It also unhide DeprecationWarning.
    """
    if not sys.warnoptions:
        # Route warnings through python logging
        logging.captureWarnings(True)

        # DeprecationWarning is by default hidden, hence we force the
        # "default" behavior on deprecation warnings which is not to hide
        # errors.
        warnings.simplefilter("default", DeprecationWarning)


def load_config(app, module_name, **kwargs_config):
    """Load configuration.

    Configuration is loaded from:

    1. Application configuration module.
    2. <instance folder>/<app name>.cfg
    3. Keyword arguments.
    """
    # Load site specific default configuration
    app.config.from_object(module_name)

    # Load <app name>.cfg from instance folder
    app.config.from_pyfile('{}.cfg'.format(app.name), silent=True)

    # Update application config from parameters.
    app.config.update(kwargs_config)

    # Ensure SECRET_KEY is set.
    SECRET_KEY = app.config.get('SECRET_KEY', 'change_me')

    if not SECRET_KEY or SECRET_KEY == 'change_me':
        fill_secret_key = """
    Set variable SECRET_KEY with random string in %s.cfg.
    """ % (app.name, )
        warnings.warn(fill_secret_key, UserWarning)

    app.config["SECRET_KEY"] = SECRET_KEY


def load_application(app):
    """Load application.

    Assembles the application by use of PACKAGES and EXTENSIONS configuration
    variables.
    """
    # Initialize application registry, used for discovery and loading of
    # configuration, extensions and blueprints
    Registry(app=app)

    # Register packages listed in PACKAGES conf variable.
    app.extensions['registry']['packages'] = PackageRegistry(app)

    # Extend application config with configuration from packages (app config
    # takes precedence)
    ConfigurationRegistry(app)

    # Register extensions listed in EXTENSIONS conf variable.
    app.extensions['registry']['extensions'] = ExtensionRegistry(app)

    # Register blueprints from packages in PACKAGES conf variable.
    app.extensions['registry']['blueprints'] = \
        BlueprintAutoDiscoveryRegistry(app=app)


def create_base_app(app_name, instance_path=None):
    """Create a base Flask Application."""
    configure_warnings()

    # Force instance folder to always be located in under system prefix
    instance_path = instance_path or os.path.join(
        sys.prefix, 'var', app_name + '-instance'
    )

    # Create instance path
    try:
        if not os.path.exists(instance_path):
            os.makedirs(instance_path)
    except Exception:
        pass

    # Create the Flask application instance
    app = Flask(
        app_name,
        static_url_path='/static/',
        static_folder=os.path.join(instance_path, 'static'),
        template_folder='templates',
        instance_relative_config=True,
        instance_path=instance_path,
    )

    # Handle both URLs with and without trailing slashes by Flask.
    # @blueprint.route('/test')
    # @blueprint.route('/test/') -> not necessary when strict_slashes == False
    app.url_map.strict_slashes = False

    return app


def create_app(app_name, module_name, **kwargs_config):
    """Create a Flask application."""
    app = create_base_app(app_name)
    load_config(app, module_name, **kwargs_config)
    load_application(app)
    return app
