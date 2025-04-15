import os
import time
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson import ObjectId




load_dotenv()

app = Flask(__name__, static_folder="static")

mongo_url = os.getenv("MONGO_URI")
app.config["MONGO_URI"] =  mongo_url + "/users_database"

mongo = PyMongo(app)

CORS(app)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_static_files(path):
    if path == "" or path == "index.html":
        
        return send_from_directory(app.static_folder, "index.html")
    else:
      
        return send_from_directory(app.static_folder, path)
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
# Endpoints
@app.route('/api/users')
def index():
    try:
        users = list(mongo.db.users.find({}))
        for user in users:
            user["_id"] = str(user["_id"])

        return jsonify(users), 200
    
    except Exception as e:
        return jsonify({"message",f"error: {e}"}), 500

@app.route("/api/users/new", methods=['POST'])
def create_user():
    try:
        data = request.json
        data['created_ts'] = float(int(time.time()))

        mongo.db.users.insert_one(data)

        return jsonify({"message":"User successfully created"}), 201
    except Exception as e:
        return jsonify({"message":f"error: {e}"}), 500

@app.route("/api/users/<id>")
def get_user(id):
    user = mongo.db.users.find_one({"_id": ObjectId(id)})
    if not user:
        return jsonify({"message":"User not found"}),404
    
    user["_id"] = str(user["_id"])
    return jsonify(user),200

@app.route("/api/users/<id>", methods=['PUT'])
def update_user(id):
        data = request.json

        data["updated_ts"] = float(int(time.time()))

        result = mongo.db.users.update_one({"_id": ObjectId(id)}, {"$set":data})

        if result.matched_count == 0:
            return jsonify({"message":"User not found"})
        return jsonify({"message": "User successfuly updated"}),200

@app.route("/api/users/<id>", methods=['DELETE'])
def remove_user(id):
  
    result = mongo.db.users.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"message":"User not found"})
    return jsonify({"message": "User successfuly removed"}),200


if __name__ == "__main__":
    app.run(debug=True)