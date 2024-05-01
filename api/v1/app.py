#!/usr/bin/python3
"""
create flask app, and register the blueprint app_views
to the Flask app.
"""

from os import getenv
from flask import Flask
from api.v1.views import app_views
from models import storage


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """teardown the app"""
    storage.close()


if __name__ == '__main__':
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int(getenv('BNB_API_PORT', '5000'))
    app.run(host=HOST, port=PORT, threaded=True)
