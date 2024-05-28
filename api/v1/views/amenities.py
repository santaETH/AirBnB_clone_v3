#!/usr/bin/python3
""" A script that defines views for Amenity objects"""
from flask import Flask, Blueprint, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects"""
    amenity = storage.all(Amenity).values()
    amenty_list = []
    for amenity in amenity:
        amenty_list.append(amenity.to_dict())
    return jsonify(amenty_list)


@app_views.route('amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """ Retrieves an Amenity object"""
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amnty(amenity_id):
    """ Deletes an Amenity object """
    amnty = storage.get("Amenity", amenity_id)
    if not amnty:
        abort(404)
    storage.delete(amnty)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amnty():
    """ it creates an Amenity object """
    if not request.json:
        abort(400, "Not a JSON")
    if "name" not in request.json:
        abort(400, "Missing name")
    data = request.json
    new_data = Amenity(**data)
    storage.new(new_data)
    storage.save()
    return jsonify(new_data.to_dict()), 201


@app_views.route('amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amnty(amenity_id):
    """ it updates an Amenity object """
    amnty = storage.get("Amenity", amenity_id)
    if not amnty:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amnty, k, v)
    storage.save()
    return jsonify(amnty.to_dict()), 200
