import os

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from db import db
from blocklist import BLOCKLIST
import models
from resources.translations import blp as TranslationBlueprint
from resources.users import blp as UserBlueprint
from resources.transcription import blp as TranscriptionBluepirnt

def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type","Authorization"])  # This will enable CORS for all routes
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Chadia Ai Youtube Videos Scripts Generator"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    #app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///database.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///databse10.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['CORS_HEADERS'] = 'Content-Type'

    db.init_app(app)

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "juba"
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_revoked",
            "description": "The token has been revoked"
        }), 401


    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "token_expired",
            "message": "The token has expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            "error": "invalid_token",
            "message": "Signature verification failed"
        }), 401

    @jwt.unauthorized_loader
    def unauthorized_token_callback(error):
        return jsonify({
            "error": "authorized_required",
            "message": "Request does not contain an access token"
        }), 401


    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            "error": "fresh_token_required",
            "description": "The token is not fresh"
        }), 401


    @app.before_first_request

    #with app.app_context():
    def create_tables():
        db.create_all()

    app.register_blueprint(TranslationBlueprint)
    app.register_blueprint(UserBlueprint)
    app.register_blueprint(TranscriptionBluepirnt)

    return app



