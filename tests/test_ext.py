# -*- coding: utf-8 -*-
#
# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or
# modify it under the terms of the Revised BSD License; see LICENSE
# file for more details.

from __future__ import absolute_import

from .helpers import FlaskTestCase
from flask_appfactory import AppFactory


class TestAppFactory(FlaskTestCase):
    """
    Tests of extension creation
    """
    def test_version(self):
        # Assert that version number can be parsed.
        from flask_appfactory import __version__
        from distutils.version import LooseVersion
        LooseVersion(__version__)

    def test_creation(self):
        assert 'appfactory' not in self.app.extensions
        AppFactory(app=self.app)
        assert isinstance(self.app.extensions['appfactory'], AppFactory)

    def test_creation_old_flask(self):
        # Simulate old Flask (pre 0.9)
        del self.app.extensions
        AppFactory(app=self.app)
        assert isinstance(self.app.extensions['appfactory'], AppFactory)

    def test_creation_init(self):
        assert 'appfactory' not in self.app.extensions
        r = AppFactory()
        r.init_app(app=self.app)
        assert isinstance(self.app.extensions['appfactory'], AppFactory)

    def test_double_creation(self):
        AppFactory(app=self.app)
        self.assertRaises(RuntimeError, AppFactory, app=self.app)
