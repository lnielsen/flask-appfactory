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
from flask_appfactory.apackage.amodule import AClass


class TestAClass(FlaskTestCase):
    """
    Tests of Aclass
    """
    def test_init(self):
        a = AClass(None)
        assert a.a is None
