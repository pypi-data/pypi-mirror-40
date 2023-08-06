"""a simple Flask app
"""
__version__ = """
0.2.1-dev0
""".strip()

import os
import flask

TEMPLATE = "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Hello</title></head><body>hello {} from %d (%s)</body></html>" % (os.getpid(),__version__)

app = flask.Flask(__name__)


def counter(start=1):
    while True:
        yield start
        start += 1


visits = counter().__next__


@app.route("/")
def hello():
    return TEMPLATE.format(visits())
