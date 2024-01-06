#!/usr/bin/python3
"""handles api requests to the User object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
def get_all_users():
    """return all user objects in storage"""
    all_users = storage.all('User')
    all_users_list = []
    for user in all_users.values():
        all_users_list.append(user.to_dict())
    return (jsonify(all_users_list))


@app_views.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """return a single User instance or 404 if not found"""
    user = storage.get('User', user_id)
    if (user is None):
        abort(404)
    return (jsonify(user.to_dict()))


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """deletes a user object from storage"""
    user = storage.get('User', user_id)
    if (user is None):
        abort(404)
    storage.delete(user)
    storage.save()
    return ({}, 200)


@app_views.route('/users', methods=['POST'])
def create_new_user():
    """create new user"""
    user_dict = request.get_json(silent=True)
    if not user_dict:
        abort(400, 'Not a JSON')
    if 'email' not in user_dict:
        abort(400, 'Missing email')
    if 'password' not in user_dict:
        abort(400, 'Missing password')

    new_user = User(**user_dict)
    new_user.save()
    return (jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """update existing user"""

    user_dict = request.get_json(silent=True)
    if not user_dict:
        abort(400, 'Not a JSON')

    user = storage.get('User', user_id)
    if user is None:
        abort(404)

    for key, value in user_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key == 'email':
            continue
        setattr(user, key, value)
    user.save()
    return (jsonify(user.to_dict()), 200)
