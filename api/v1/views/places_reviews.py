#!/usr/bin/python3
"""
create a new view for Place objects
that handles all default RESTFul API actions
"""
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_by_place(place_id):
    """return the list of all reviews objs of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({'message': 'Not found'}), 404

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """return a review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'error': 'Not found'}), 404

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'message': 'Not found'}), 404

    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """create a new review obj"""
    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400
    place = storage.get(Place, place_id)
    if not place:
        return jsonify({'message': 'Not found'}), 404
    if not request.get_json():
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({'message': 'Missing user_id'}), 400
    if 'text' not in data:
        return jsonify({'message': 'Missing text'}), 400

    user = storage.get(User, data['user_id'])
    if not user:
        return jsonify({'message': 'Not found'}), 404

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """update a review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        return jsonify({'message': 'Not found'}), 404

    if request.content_type != 'application/json':
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'message': 'Not a JSON'}), 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at',
                       'updated_at']:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_dict()), 200
