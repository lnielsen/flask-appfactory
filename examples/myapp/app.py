"""Flask application."""

from flask_appfactory import appfactory


def create_app(load=True, **kwargs_config):
    """Flask application factory."""
    return appfactory("myapp", "myapp.config", load=load, **kwargs_config)
