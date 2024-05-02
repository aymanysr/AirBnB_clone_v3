#!/usr/bin/python3
"""
create a new view for City objects
that handles all default RESTFul API actions
"""
from flask import jsonify, request
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_by_state(state_id):
    """return the list of all cities objs of a state"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({'message': 'Not found'}), 404

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """return a city obj"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete a city obj"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'message': 'Not found'}), 404

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create a new city obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if not state:
        return jsonify({'message': 'Not found'}), 404
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({'message': 'Missing name'}), 400
    data['state_id'] = state_id

    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """update a city obj"""
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({'message': 'Not found'}), 404

    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Not a JSON'}), 400

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
