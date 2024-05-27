#!/usr/bin/python3
""" A script that defines views for State objects that"""
from flask import Flask, abort, jsonify, Blueprint, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """GET /states - Returns all states"""
    states = storage.all("State").values()
    if not states:
        abort(404)
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>', methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """GET /states/<state_id> - Returns a state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """DELETE /states/<state_id> - Deletes a state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """POST /states - Creates a new state"""
    if not request.get_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json()
    new_data = State(**data)
    new_data.save()
    return jsonify(new_data.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """PUT /states/<state_id> - Updates a state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json:
        abort(400,  description="Not a JSON")
    state_data = request.get_json()

    for k, v in state_data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
