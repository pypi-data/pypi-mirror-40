"""a simple Flask app
"""
__version__ = """
0.2.0-dev5
""".strip()

import os
import flask

TEMPLATE = "hello {} from %d (%s)" % (os.getpid(),__version__)

app = flask.Flask(__name__)


def counter(start=1):
    while True:
        yield start
        start += 1


visits = counter().__next__


@app.route("/")
def hello():
    return TEMPLATE.format(visits())
