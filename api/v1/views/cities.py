#!/usr/bin/python3
"""Main application script"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.state import City
from models.city import City
import os
app = Flask(__name__)


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id=None):
    """Retrieve cities by state"""
    states = storage.all('State')
    state = states.get('State' + '.' + state_id)
    if state is None:
        abort(404)
    city_list = []
    cities = storage.all('City')
    for city in cities.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list), 200


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """Retrieve city object"""
    city_dict = storage.all('City')
    city = city_dict.get('City' + "." + city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id=None):
    """Delete a city object"""
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id=None):
    """Create a new city object"""
    state_dict = storage.all('State')
    state = state_dict.get('State' + "." + state_id)
    if state is None:
        abort(404)
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in result:
        return jsonify({"error": "Missing name"}), 400
    obj = City(name=result['name'], state_id=state_id)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id=None):
    """Update a city object"""
    result = request.get_json()
    if result is None:
        return jsonify({"error": "Not a JSON"}), 400
    obj = storage.get('City', city_id)
    if obj is None:
        abort(404)
    invalid_keys = ["id", "created_at", "updated_at"]
    for key, value in result.items():
        if key not in invalid_keys:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200
