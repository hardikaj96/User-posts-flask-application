from flask import Flask, request, jsonify
from services import PostsService
from models import Schema

import json

app = Flask(__name__)


@app.after_request
def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] =  "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods']=  "POST, GET, PUT, DELETE, OPTIONS"
    return response


@app.route("/")
def index():
    return jsonify(desc="Welcome to Users and Posts application")


@app.route("/<name>")
def index_user(name):
    return jsonify(desc="Welcome "+name+"to Users and Posts application") 


@app.route("/posts", methods=["GET"])
def list_post():
    return jsonify(PostsService().list())


@app.route("/posts", methods=["POST"])
def create_post():
    return jsonify(PostsService().create(request.get_json()))


@app.route("/posts/<post_id>", methods=["PUT"])
def update_post(post_id):
    return jsonify(PostsService().update(post_id, request.get_json()))


@app.route("/posts/<post_id>", methods=["DELETE"])
def delete_post(post_id):
    return jsonify(PostsService().delete(post_id))


if __name__ == "__main__":
    Schema()
    app.run(debug=True, port=8888)