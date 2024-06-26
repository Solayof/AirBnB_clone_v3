#!/usr/bin/python3
"""State route blueprint view"""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def states():
    """Retrieves the list of all states if
    no state id otherwise the list of the provided state id
    """
    if request.method == "GET":
        return jsonify([
            state.to_dict() for state in storage.all("State").values()
        ])
    reqs = request.get_json(silent=True)
    if not reqs:
        return "Not a JSON", 400
    if not reqs.get("name"):
        return "Missing name", 400
    obj = State(**reqs)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["DELETE", "GET", "PUT"])
def state_id(state_id=None):
    """handle DELETE, PUT and GET methods"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == "GET":
        return jsonify(state.to_dict())
    if request.method == "DELETE":
        state.delete()
        storage.save()
        return jsonify({})
    reqs = request.get_json(silent=True)
    if not reqs:
        return "Not a JSON", 400

    for k, v in reqs.items():
        if k not in ["id", "updated_at", "created_at"]:
            setattr(state, k, v)

    state.save()
    return jsonify(state.to_dict())
