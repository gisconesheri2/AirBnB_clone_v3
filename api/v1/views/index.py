from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods = ['GET'])
def show_status():
    """return a JSON OK message"""
    return jsonify({'status' : 'OK'})
