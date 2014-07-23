# -*- coding: utf-8 -*-

"""Flask-Restful extensions initialization."""

from __future__ import absolute_import, unicode_literals, print_function

from flask.ext.restful import Api
from flask.ext.registry import ModuleAutoDiscoveryRegistry


def setup_app(app):
    """Setup Flask-Restful."""
    api = Api(app)
    app.extensions['restful'] = api

    class RestfulRegistry(ModuleAutoDiscoveryRegistry):
        setup_func_name = 'init_api'

        def register(self, module, *args, **kwargs):
            return super(RestfulRegistry, self).register(module, app, api,
                                                         *args, **kwargs)

    app.extensions['registry']['restful'] = RestfulRegistry(
        'restful', app=app, with_setup=True
    )
