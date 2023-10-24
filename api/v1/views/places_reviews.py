#!/usr/bin/python3
"""objects that handle all default REStfull api actions for reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """retrives the list of reviews"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """retrives a review of objects"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}, 200))


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """create a review"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    user_id = request.get_json()['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data = request.get_json()
    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """update a review object"""
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
