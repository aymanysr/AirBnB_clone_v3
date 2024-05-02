#!/usr/bin/python3
"""
create a new view for amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """return the list of all user objs"""
    users = storage.all(User).values()
    user_list = [user.to_dict() for user in users]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """return a user obj"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user obj"""
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_user():
    """create a new user obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    kwargs = request.get_json()

    if 'email' not in kwargs:
        return jsonify({'message': 'Missing email'}), 400
    if 'password' not in kwargs:
        return jsonify({'message': 'Missing password'}), 400

    new_user = User(**kwargs)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update a user obj"""
    user = storage.get(User, user_id)

    if user:
        if request.content_type != 'application/json':
            return jsonify({'message': 'Not a JSON'}), 400
        if not request.get_json():
            return jsonify({'message': 'Not a JSON'}), 400

        kwargs = request.get_json()
        for key, value in kwargs.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'Not found'}), 404
