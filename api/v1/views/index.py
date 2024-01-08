#!/usr/bin/python3
"""define blueprint routes for the index page"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'])
def show_status():
    """return a JSON OK message"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count_objects():
    """return number of each object in storage"""
    classes = ['Amenity', 'City', 'Place', 'Review', 'State', 'User']
    cls_str = ['amenities', 'cities', 'places', 'reviews',
               'states', 'users']
    return_dict = {}
    i = 0
    for cls in classes:
        return_dict[cls_str[i]] = storage.count(cls)
        i += 1
    return jsonify(return_dict)
