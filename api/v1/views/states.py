#!/usr/bin/python3
"""handles api requests to the State object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """return all state objects in storage"""
    all_states = storage.all('State')
    all_states_list = []
    for state in all_states.values():
        all_states_list.append(state.to_dict())
    return (jsonify(all_states_list))


@app_views.route('/states/<state_id>', methods=['GET'])
def get_single_state(state_id):
    """return a single State instance or 404 if not found"""
    state = storage.get('State', state_id)
    if (state is None):
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """deletes a state object from storage"""
    state = storage.get('State', state_id)
    if (state is None):
        abort(404)
    storage.delete(state)
    storage.save()
    return ({}, 200)


@app_views.route('/states', methods=['POST'])
def create_new_state():
    """create new state"""
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state_dict = request.get_json()
    new_state = State(**state_dict)
    new_state.save()
    return (jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update existing state"""
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')

    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    state_dict = request.get_json()
    for key, value in state_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        setattr(state, key, value)
    state.save()
    return (jsonify(state.to_dict()), 200)
