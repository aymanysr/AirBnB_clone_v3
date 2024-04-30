#!/usr/bin/python3
"""
create flask app; app_views
"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
    """return status"""
    resp = {"status": "OK"}
    return jsonify(resp)
