#!/usr/bin/python3
"""
create a new view for Place objects
that handles all default RESTFul API actions
"""
from flask import jsonify, request
from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places_by_city(city_id):
    """return the list of all places objs of a city"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'message': 'Not found'}), 404

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """return a place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'message': 'Not found'}), 404

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create a new place obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    city = storage.get(City, city_id)
    if not city:
        return jsonify({'message': 'Not found'}), 404
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'message': 'Missing user_id'}), 400
    if 'name' not in data:
        return jsonify({'message': 'Missing name'}), 400

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """update a place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'message': 'Not found'}), 404

    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
