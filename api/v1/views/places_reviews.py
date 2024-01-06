#!/usr/bin/python3
"""handles api requests to the Review object"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_all_reviews(place_id):
    """return all review objects associated with place_id in storage"""
    place = storage.get('Place', place_id)
    if (place is None):
        abort(404)

    place_reviews = place.reviews
    all_reviews_list = []
    for review in place.reviews:
        all_reviews_list.append(review.to_dict())
    return (jsonify(all_reviews_list))


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_single_review(review_id):
    """return a single Review instance or 404 if not found"""
    review = storage.get('Review', review_id)
    if (review is None):
        abort(404)
    return (jsonify(review.to_dict()))


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """deletes a review object from storage"""
    review = storage.get('Review', review_id)
    if (review is None):
        abort(404)
    storage.delete(review)
    storage.save()
    return ({}, 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_new_review(place_id):
    """create new review"""

    place = storage.get('Place', place_id)
    if (place is None):
        abort(404)

    review_dict = request.get_json(silent=True)
    if not review_dict:
        abort(400, 'Not a JSON')

    if ('user_id' not in review_dict):
        abort(400, 'Missing user_id')
    user = storage.get('User', review_dict['user_id'])
    if (user is None):
        abort(404)

    if 'text' not in review_dict:
        abort(400, 'Missing text')

    review_dict['place_id'] = place.id
    new_review = Review(**review_dict)
    new_review.save()
    return (jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """update existing review"""

    review_dict = request.get_json(silent=True)
    if not review_dict:
        abort(400, 'Not a JSON')

    review = storage.get('Review', review_id)
    if review is None:
        abort(404)

    for key, value in review_dict.items():
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key == 'place_id':
            continue
        if key == 'user_id':
            continue
        setattr(review, key, value)
    review.save()
    return (jsonify(review.to_dict()), 200)
