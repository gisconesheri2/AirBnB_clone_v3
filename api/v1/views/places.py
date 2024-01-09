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


@app_views.route('/places_search', methods=['POST'])
def search_place():
    """search Places with a query parameters in a json string"""
    search_dict = request.get_json(silent=True)
    if search_dict is None:
        abort(400, 'Not a JSON')

    states_terms = search_dict.get('states', None)
    cities_terms = search_dict.get('cities', None)
    amenities_terms = search_dict.get('amenities', None)
    print(search_dict)
    if (len(search_dict) == 0):
        all_places = storage.all('Place')
        all_places_list = []
        for place in all_places.values():
            all_places_list.append(place.to_dict())
        return (jsonify(all_places_list))

    if ((states_terms is None) and
            (cities_terms is None) and
            (amenities_terms is None)):
        # if all search keys are empty return all Places
        all_places = storage.all('Place')
        all_places_list = []
        for place in all_places.values():
            all_places_list.append(place.to_dict())
        return (jsonify(all_places_list))

    all_places_ids = []
    all_places_list = []
    if (states_terms is not None):
        for state_id in states_terms:
            state_obj = storage.get('State', state_id)
            state_cities = state_obj.cities
            for city in state_cities:
                places = city.places
                for place in places:
                    if place.id not in all_places_ids:
                        all_places_ids.append(place.id)
                        all_places_list.append(place.to_dict())

    if (cities_terms is not None):
        for city_id in cities_terms:
            city_obj = storage.get('City', city_id)
            city_places = city_obj.places
            for place in city_places:
                if place not in all_places_ids:
                    all_places_ids.append(place.id)
                    all_places_list.append(place.to_dict())

    if ((amenities_terms is not None) and
            (states_terms is None) and
            (cities_terms is None)):
        all_places = storage.all('Place')
        for place in all_places.values():
            all_places_ids.append(place.id)
            all_places_list.append(place.to_dict())

    if (amenities_terms is not None):
        all_places_list = []
        place_amenity_ids = []
        found = False
        for place_id in all_places_ids:
            place_obj = storage.get('Place', place_id)
            place_amenities = place_obj.amenities
            for place_amenity in place_amenities:
                place_amenity_ids.append(place_amenity.id)
            for am_id in amenities_terms:
                if am_id in place_amenity_ids:
                    found = True
                else:
                    found = False
                    break
            if found is True:
                place_obj_dict = place_obj.to_dict()
                place_obj_dict.pop('amenities')
                all_places_list.append(place_obj_dict)

    return (jsonify(all_places_list))
