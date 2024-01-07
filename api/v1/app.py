#!/usr/bin/python3
"""app functionality"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from models import storage, storage_t
from os import getenv

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})

app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """return a custom json error"""
    return (make_response(jsonify({'error': 'Not found'}), 404))


@app.teardown_appcontext
def shut_db(exception):
    """close the database session"""
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", default="0.0.0.0")
    port = getenv("HBNB_API_PORT", default="5000")

    app.run(host=host, port=port, threaded=True)
