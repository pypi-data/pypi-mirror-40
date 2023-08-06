"""a simple Flask app
"""
__version__='0.1'

import flask

app = flask.Flask(__name__)

def counter(start=1):
  while True:
    yield start
    start+=1

visits = counter().__next__

@app.route("/")
def hello():
  return "hello {}".format(visits())
