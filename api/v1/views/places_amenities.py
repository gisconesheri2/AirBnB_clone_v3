#!/usr/bin/python3
"""handles api requests to the Place-Amenity  objects relationship"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage, storage_t


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_all_place_amenities(place_id):
    """return all amenity objects associated with place_id in storage"""
    place = storage.get('Place', place_id)
    if (place is None):
        abort(404)

    place_amenities = place.amenities
    all_amenities_list = []
    for amenity in place_amenities:
        all_amenities_list.append(amenity.to_dict())
    return (jsonify(all_amenities_list))


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenity_from_place(place_id, amenity_id):
    """deletes an Amenity object from Place instance"""
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if (amenity is None):
        abort(404)
    if (place is None):
        abort(404)

    if (storage_t == 'db'):
        try:
            place.amenities.remove(amenity)
        except Exception:
            abort(404)
    else:
        try:
            delattr(amenity, "place_id")
            place.amenity_ids.remove(amenity.id)
        except Exception:
            abort(404)

    storage.save()
    return ({}, 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_place_new_amenity(place_id, amenity_id):
    """create new link between a Place and an Amenity"""

    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if (amenity is None):
        abort(404)
    if (place is None):
        abort(404)

    if (storage_t == 'db'):
        if amenity not in place.amenities:
            place.amenities.append(amenity)
            storage.save()
            return (jsonify(amenity.to_dict()), 201)
    else:
        if amenity.id not in place.amenity_ids:
            place.amenity_ids.append(amenity.id)
            storage.save()
            return (jsonify(amenity.to_dict()), 201)
    return (jsonify(amenity.to_dict()), 200)
