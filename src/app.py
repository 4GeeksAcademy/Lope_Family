"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")

"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# 1) GET /members → devuelve TODOS los miembros (lista)
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    # El enunciado y los tests esperan una LISTA directamente
    return jsonify(members), 200


# 2) GET /members/<int:member_id> → devuelve UN miembro
@app.route('/members/<int:member_id>', methods=['GET'])
def get_single_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        # 404 si no existe
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200


# 3) POST /members → añade un miembro nuevo
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()

    # Si no llega JSON, error 400
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400

    # Campos mínimos según el enunciado
    required_fields = ["first_name", "age", "lucky_numbers"]
    missing = [f for f in required_fields if f not in body]
    if missing:
        return jsonify({
            "error": "Missing fields",
            "missing": missing
        }), 400

    # El id es opcional (si no viene, lo genera _generate_id)
    new_member = {
        "id": body.get("id"),
        "first_name": body["first_name"],
        "age": body["age"],
        "lucky_numbers": body["lucky_numbers"]
    }

    created = jackson_family.add_member(new_member)
    # Los tests esperan 200 con el miembro creado en JSON
    return jsonify(created), 200


# 4) DELETE /members/<int:member_id> → elimina un miembro
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    deleted = jackson_family.delete_member(member_id)
    if not deleted:
        # Si no existía ese id
        return jsonify({"error": "Member not found"}), 404

    # El enunciado pide que el body tenga { "done": True }
    return jsonify({"done": True}), 200


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
