#!/usr/bin/python3
""" A rest api for cities objects """
from flask import Flask, abort, request, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """it retrieves the list of all City objects in a State """
    city_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())

    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """it retrieves a City object """
    city = storage.get('City', city_id)

    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """it deletes a City object """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ it creates a City object"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    data = request.json
    new_data = City(**data)
    new_data.state_id = state_id
    storage.new(new_data)
    storage.save()
    return jsonify(new_data.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """it updates a City object """
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
