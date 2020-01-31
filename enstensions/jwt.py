import webapp.api as API
from flask_jwt_extended import JWTManager


API.jwt     = JWTManager()
