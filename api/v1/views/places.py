#!/usr/bin/python3
"""handles api requests to the Place object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.place import Place
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_all_places(city_id):
    """return all place objects associated with city_id in storage"""
    city = storage.get('City', city_id)
    if (city is None):
        abort(404)

    places = city.places
    all_places_list = []
    for place in places:
        all_places_list.append(place.to_dict())
    return (jsonify(all_places_list))


@app_views.route('/places/<place_id>', methods=['GET'])
def get_single_place(place_id):
    """return a single Place instance or 404 if not found"""
    place = storage.get('Place', place_id)
    if (place is None):
        abort(404)
    return (jsonify(place.to_dict()))


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """deletes a place object from storage"""
    place = storage.get('Place', place_id)
    if (place is None):
        abort(404)
    storage.delete(place)
    storage.save()
    return ({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_new_place(city_id):
    """create new place"""

    city = storage.get('City', city_id)
    if (city is None):
        abort(404)

    place_dict = request.get_json(silent=True)
    if not place_dict:
        abort(400, 'Not a JSON')

    if 'user_id' not in place_dict:
        abort(400, 'Missing user_id')
    user = storage.get('User', place_dict['user_id'])
    if (user is None):
        abort(404)

    if 'name' not in place_dict:
        abort(400, 'Missing name')

    place_dict['city_id'] = city.id
    new_place = Place(**place_dict)
    new_place.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """update existing place"""
    if not request.get_json(silent=True):
        abort(400, 'Not a JSON')

    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    place_dict = request.get_json()
    for key, value in place_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key == 'user_id':
            continue
        if key == 'city_id':
            continue
        setattr(place, key, value)
    place.save()
    return (jsonify(place.to_dict()), 200)
