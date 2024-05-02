#!/usr/bin/python3
"""
create flask app; app_views
"""

from flask import jsonify, abort, request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """return the list of all states objs"""
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', strict_slashes=False)
def get_state(state_id):
    """return a state obj"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state obj"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """create a new state obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return jsonify({'message': 'Missing name'}), 400

    new_state = State(**kwargs)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state obj"""

    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return jsonify({'message': 'Not a JSON'}), 400
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    return jsonify({'message': 'Not found'}), 404
