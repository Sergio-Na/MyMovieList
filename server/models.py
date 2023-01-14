from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from app import db
from flask_jwt_extended import create_access_token
import jwt
from app import app
import requests


class User:

    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "username": request.get_json()['username'],
            "email": request.get_json()['email'],
            "password": request.get_json()['password'],
            "reviews": []
        }
        oldPass = user['password']
        user['password'] = generate_password_hash(user['password'])

        # Check for duplicate email
        if db.users.find_one({"email": user['email']}):
            print(db.users.find_one({"email": user["email"]}))
            print((db.users.find_one({"email": user["email"]}))['email'])

            return jsonify({"error": "Email already exitst"}), 400

        # Check for duplicate username
        if db.users.find_one({"username": user['username']}):
            return jsonify({"error": "Username already exitst"}), 400

        if db.users.insert_one(user):
            return self.login(password=oldPass, email=user['email'])

        return jsonify({"error": "Signup failed"}), 400

    def login(self, password, email):

        curUser = db.users.find_one({"email": email})
        print(curUser)
        if curUser:
            if check_password_hash(curUser['password'], password):
                access_token = create_access_token(identity=email)
                return jsonify({"token": access_token}), 200
            else:
                return jsonify({"error": "Incorrect Password"}), 403
        else:
            return jsonify({"error": "User does not exist"}), 404

    def add_review(self):
        token = request.get_json()['token']
        movie_id = request.get_json()['movie_id']
        email = jwt.decode(
            token, app.config["JWT_SECRET_KEY"], algorithms=['HS256'])['sub']
        review = request.get_json()['review']
        return jsonify(db.users.find_one_and_update({"email": email}, {'$push': {"reviews": {movie_id: review}}})), 200

    def get_reviews(self):
        token = request.get_json()['token']
        email = jwt.decode(
            token, app.config["JWT_SECRET_KEY"], algorithms=['HS256'])['sub']
        reviews = db.users.find_one({"email": email})['reviews']
        return jsonify(reviews), 200
