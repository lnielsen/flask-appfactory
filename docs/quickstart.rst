.. _quickstart:

Quickstart
==========

This guide assumes you have successfully installed Flask-AppFactory and a working
understanding of Flask. If not, follow the installation steps and read about
Flask at http://flask.pocoo.org/docs/.


A Minimal Example
-----------------

A minimal Flask-AppFactory usage example looks like this. First create the
application and initialize the extension:

>>> from flask import Flask
>>> from flask_appfactory import AppFactory
>>> app = Flask('myapp')
>>> ext = AppFactory(app=app)

Some Extended Example
---------------------
Flask-AppFactory also has support for CHANGEME

.. literalinclude:: ../tests/helpers.py
