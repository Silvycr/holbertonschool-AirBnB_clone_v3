#!/usr/bin/python3
"""objects that handle all default REStfull APi actions for states"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """retrieves the list of all state objects"""
    all_states = storage.all(State).values()
    list_states = []
    for state in all_states:
        list_states.append(state.to_dict())
    return jsonify(list_states)


@app_views.route("states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """retrieves a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """delete a state object"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify({}, 200))


@app_views.route("/states/", methods=["POST"])
def post_state():
    """create a state"""
    if not request.get_json():
        abort(400, description="Note a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"])
def update_state(state_id):
    """update states objects"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
