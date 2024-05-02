#!/usr/bin/python3
"""
create a new view for amenity objects
that handles all default RESTFul API actions
"""
from flask import jsonify, request
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenities():
    """return the list of all amenities objs"""
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """return a amenity obj"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete a amenity obj"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return jsonify({'message': 'Not found'}), 404


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create a new amenity obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400
    kwargs = request.get_json()

    if 'name' not in kwargs:
        return jsonify({'message': 'Missing name'}), 400

    new_amenity = Amenity(**kwargs)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """update a amenity obj"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        if request.content_type != 'application/json':
            return jsonify({'message': 'Not a JSON'}), 400
        kwargs = request.get_json()

        if not kwargs:
            return jsonify({'message': 'Not a JSON'}), 400

        for key, value in kwargs.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    return jsonify({'message': 'Not found'}), 404
