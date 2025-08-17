"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, jsonify, request
import random
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)


class Family:
    def __init__(self):
        # Inicializamos con 3 miembros
        self.members = [
            {
                "id": 1,
                "first_name": "John",
                "age": 33,
                "lucky_numbers": [7, 13, 22]
            },
            {
                "id": 2,
                "first_name": "Jane",
                "age": 35,
                "lucky_numbers": [10, 14, 3]
            },
            {
                "id": 3,
                "first_name": "Jimmy",
                "age": 5,
                "lucky_numbers": [1]
            }
        ]
        self.next_id = 4

    def get_all_members(self):
        return self.members

    def add_member(self, member):
        member_id = member.get("id", self.next_id)
        member["id"] = member_id
        self.members.append(member)
        self.next_id += 1
        return member

    def get_member(self, member_id):
        for m in self.members:
            if m["id"] == member_id:
                return m
        return None

    def delete_member(self, member_id):
        member = self.get_member(member_id)
        if member:
            self.members.remove(member)
            return True
        return False

# Instanciamos la familia
family = Family()

# Rutas
@app.route("/members", methods=["GET"])
def get_members():
    return jsonify(family.get_all_members())

@app.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    member = family.get_member(member_id)
    if member:
        return jsonify(member)
    return jsonify({"error": "Member not found"}), 404

@app.route("/members", methods=["POST"])
def add_member():
    data = request.get_json()
    new_member = {
        "first_name": data["first_name"],
        "age": data["age"],
        "lucky_numbers": data["lucky_numbers"]
    }
    added_member = family.add_member(new_member)
    return jsonify(added_member)

@app.route("/members/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    success = family.delete_member(member_id)
    return jsonify({"done": success})

if __name__ == "__main__":
    app.run(debug=True)
