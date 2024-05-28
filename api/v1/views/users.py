#!/usr/bin/python3
""" A script that defines views for User objects"""
from flask import Flask, abort, request, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_usrs():
    """" it retrieves the list of all User objects"""
    usrs = storage.all("User").values()
    if not usrs:
        abort(404)
    return jsonify([usr.to_dict() for usr in usrs])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_usr(user_id):
    """ it retrieves a user object"""
    usr = storage.get("User", user_id)
    if not usr:
        abort(404)
    return jsonify(usr.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_usr(user_id):
    """ it deletes a user object"""
    usr = storage.get("User", user_id)
    if not usr:
        abort(404)
    storage.delete(usr)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_usr():
    """ it creates a user object"""
    if not request.json:
        abort(400, "Not a JSON")
    if "email" not in request.json:
        abort(400, "Missing email")
    if "password" not in request.json:
        abort(400, "Missing password")
    usr_data = request.json
    new_usr_data = User(**usr_data)
    storage.new(new_usr_data)
    storage.save()
    return jsonify(new_usr_data.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_usr(user_id):
    """ it updates a user object"""
    usr = storage.get("User", user_id)
    if not usr:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    for k, v in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(usr, k, v)
    storage.save()
    return jsonify(usr.to_dict()), 200
