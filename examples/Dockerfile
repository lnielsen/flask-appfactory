# This file is part of Flask-AppFactory
# Copyright (C) 2015 CERN.
#
# Flask-AppFactory is free software; you can redistribute it and/or modify it under
# the terms of the Revised BSD License; see LICENSE file for more details.

# Use Python-2.7:
FROM python:2.7

# Add sources to `code` and work there:
ADD ./ /code

RUN pip install redis

# Install flask-appfactory:
WORKDIR /code
RUN pip install -e .[celery]

# Install example
WORKDIR /code/examples
RUN pip install -e .

# Run container as user `flask-appfactory` with UID `1000`, which should match
# current host user in most situations:
RUN adduser --uid 1000 --disabled-password --gecos '' flaskappfactory && \
    chown -R flaskappfactory:flaskappfactory /code

# Run test suite instead of starting the application:
USER flaskappfactory
CMD ["myapp", "run"]
