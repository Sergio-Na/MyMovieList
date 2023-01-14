from flask import Flask
import pymongo
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
import os
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_APP_KEY')
app.config["JWT_SECRET_KEY"] = os.environ.get('JWT_SECRET')
jwt = JWTManager(app)
CORS(app)



#Database
client = pymongo.MongoClient(os.environ.get('DATABASE_URL'))
db = client.user_login_system


import routes


if __name__ == "__main__":
    app.debug = True