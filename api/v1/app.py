#!/usr/bin/python3
"""
create flask app, and register the blueprint app_views
to the Flask app.
"""

from os import getenv
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown the app"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """return a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('HBNB_API_PORT', '5000'))
    app.run(host=HOST, port=PORT, threaded=True)
