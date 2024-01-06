#!/usr/bin/python3
"""handles api requests to the Amenity object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
def get_all_amenities():
    """return all amenity objects in storage"""
    all_amenities = storage.all('Amenity')
    all_amenities_list = []
    for amenity in all_amenities.values():
        all_amenities_list.append(amenity.to_dict())
    return (jsonify(all_amenities_list))


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_single_amenity(amenity_id):
    """return a single Amenity instance or 404 if not found"""
    amenity = storage.get('Amenity', amenity_id)
    if (amenity is None):
        abort(404)
    return (jsonify(amenity.to_dict()))


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """deletes a amenity object from storage"""
    amenity = storage.get('Amenity', amenity_id)
    if (amenity is None):
        abort(404)
    storage.delete(amenity)
    storage.save()
    return ({}, 200)


@app_views.route('/amenities', methods=['POST'])
def create_new_amenity():
    """create new amenity"""
    amenity_dict = request.get_json(silent=True)
    if not amenity_dict:
        abort(400, 'Not a JSON')
    if 'name' not in amenity_dict:
        abort(400, 'Missing name')
    new_amenity = Amenity(**amenity_dict)
    new_amenity.save()
    return (jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """update existing amenity"""

    amenity_dict = request.get_json(silent=True)
    if not amenity_dict:
        abort(400, 'Not a JSON')

    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)

    for key, value in amenity_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)
