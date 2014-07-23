# -*- coding: utf-8 -*-

"""Flask-Admin extension initialization."""

from __future__ import absolute_import, unicode_literals, print_function

from flask.ext.admin import Admin
from flask.ext.registry import ModuleAutoDiscoveryRegistry


class AdminDiscoveryRegistry(ModuleAutoDiscoveryRegistry):

    """Admin views registry."""

    setup_func_name = 'register_admin'

    def __init__(self, *args, **kwargs):
        """Initialize registry."""
        self.admin = kwargs.pop('admin', None)
        super(AdminDiscoveryRegistry, self).__init__(*args, **kwargs)

    def register(self, module, *args, **kwargs):
        """Register a admin module."""
        super(AdminDiscoveryRegistry, self).register(
            module, self.app, self.admin, *args, **kwargs
        )


def setup_app(app):
    """Register all administration views with the Flask application."""
    app.config.setdefault("ADMIN_CONFIG", dict(
        name="Admin",
        url="/admin/",
        template_mode='bootstrap3',
    ))

    # Initialize app
    admin = Admin(**app.config['ADMIN_CONFIG'])
    admin.init_app(app)

    # Create registry and run discovery
    app.extensions['registry']['admin'] = AdminDiscoveryRegistry(
        'admin', app=app, with_setup=True, admin=admin
    )
