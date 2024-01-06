#!/usr/bin/python3
"""handles api requests to the City object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """return all city objects associated with state_id in storage"""
    state = storage.get('State', state_id)
    if (state is None):
        abort(404)

    state_cities = state.cities
    all_cities_list = []
    for city in state.cities:
        all_cities_list.append(city.to_dict())
    return (jsonify(all_cities_list))


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_single_city(city_id):
    """return a single City instance or 404 if not found"""
    city = storage.get('City', city_id)
    if (city is None):
        abort(404)
    return (jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """deletes a city object from storage"""
    city = storage.get('City', city_id)
    if (city is None):
        abort(404)
    storage.delete(city)
    storage.save()
    return ({}, 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_new_city(state_id):
    """create new city"""

    state = storage.get('State', state_id)
    if (state is None):
        abort(404)

    city_dict = request.get_json(silent=True)
    if not city_dict:
        abort(400, 'Not a JSON')
    if 'name' not in city_dict:
        abort(400, 'Missing name')

    city_dict['state_id'] = state.id
    new_city = City(**city_dict)
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update existing city"""
    city_dict = request.get_json(silent=True)
    if not city_dict:
        abort(400, 'Not a JSON')

    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    for key, value in city_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key == 'state_id':
            continue
        setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 200)
