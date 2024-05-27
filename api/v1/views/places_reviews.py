#!/usr/bin/python3
""" A script that defines views for Review objects """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_rev(place_id):
    """ it retrieves the list of all Review objects """
    plc = storage.get(Place, place_id)
    if not plc:
        abort(404)
    return jsonify([review.to_dict() for review in plc.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_rev_id(review_id):
    """ Retrieves a Review object """
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_rev(review_id):
    """it deletes a Review object """
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    rev.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_rev(place_id):
    """it creates a Review object """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    review_data = request.get_json()
    if not review_data:
        abort(400, "Not a JSON")
    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    user_id = review_data['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if "text" not in review_data:
        abort(400, "Missing text")
    review = Review(**review_data)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """it updates a Review object """
    rev = storage.get("Review", review_id)
    if not rev:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")

    for k, v in request_data.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(rev, k, v)

    storage.save()
    return jsonify(rev.to_dict()), 200
