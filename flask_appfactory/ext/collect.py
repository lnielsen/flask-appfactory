# -*- coding: utf-8 -*-

"""Flask-Collect extensions initialization."""

from __future__ import absolute_import, unicode_literals, print_function

from flask.ext.collect import Collect

collect = Collect()


def setup_app(app):
    """Set the application up with the correct static root."""
    def filter_(items):
        """Filter application blueprints."""
        order = [blueprint.name for blueprint in
                 app.extensions['registry']['blueprints']]

        def _key(item):
            if item.name in order:
                return order.index(item.name)
            return -1

        return sorted(items, key=_key)

    app.config.setdefault('COLLECT_FILTER', filter_)
    app.config.setdefault('COLLECT_STATIC_ROOT', app.static_folder)
    collect.init_app(app)

    # unsetting the static_folder so it's not picked up by collect.
    class FakeApp(object):
        name = "fakeapp"
        has_static_folder = False
        static_folder = None

    collect.app = FakeApp()
