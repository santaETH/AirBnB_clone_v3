#!/usr/bin/python3
""" A script that defines views for Place objects that
handle default API actions. """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """it retrieves the list of all Place objects in a City """
    cty = storage.get('City', city_id)
    if not cty:
        abort(404)
    return jsonify([place.to_dict() for place in cty.places])


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """it retrieves a Place object """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """it deletes a Place object """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """it creates a Place object """
    cty = storage.get('City', city_id)
    if not cty:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "user_id" not in request.json:
        abort(400, "Missing user_id")
    if "name" not in request.json:
        abort(400, "Missing name")
    plc_data = request.json
    new_plc_data = Place(**plc_data)
    new_plc_data.city_id = city_id
    storage.new(new_plc_data)
    storage.save()
    return jsonify(new_plc_data.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """it updates a Place object """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
