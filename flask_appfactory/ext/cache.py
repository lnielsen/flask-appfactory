# -*- coding: utf-8 -*-

"""Flask-Cache extension initialization."""

from __future__ import absolute_import, unicode_literals, print_function

from flask.ext.cache import Cache

__all__ = ('cache', 'setup_app')

cache = Cache()


def setup_app(app):
    """Initialize Flask-Cache."""
    cache.init_app(app)
