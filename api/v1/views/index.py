#!/usr/bin/python3
"""
create flask app; app_views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def api_status():
    """return status"""
    resp = {"status": "OK"}
    return jsonify(resp)


@app_views.route('/stats')
def api_stats():
    """return stats"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
