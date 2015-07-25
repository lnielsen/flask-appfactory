"""Module blueprint."""

from flask import Blueprint, render_template

blueprint = Blueprint('mymodule', __name__)


@blueprint.route("/")
def index():
    """Example view."""
    return render_template('mymodule.html')
