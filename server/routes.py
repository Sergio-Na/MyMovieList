from flask import request
from app import app
from models import User
# Home Route


@app.route('/')
def home():
    return "Hello"


# Signup
@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


# Login
@app.route('/user/login', methods=['POST'])
def login():
    print(request.args)
    return User().login(password=request.get_json()['password'], email=request.get_json()['email'])

# Add reviews for user


@app.route('/add_review', methods=['POST'])
def add_review():
    return User().add_review()

# Get User Reviews


@app.route('/get_reviews', methods=['GET'])
def get_reviews():
    return User().get_reviews()


@app.route("/user/get_info", methods=['GET'])
def get_user_info():
    return User().get_user_info()
