from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS, cross_origin

from config import DevelopmentConfig, TestingConfig

#Inicialización
app = Flask(__name__)
app.config.from_object(TestingConfig)

#API
api = Api(app)

#base de datos
db = SQLAlchemy(app)
ma = Marshmallow(app)

#seguridad
auth = HTTPBasicAuth()

#cors
cors = CORS(app, resources={r"/api/*":{"origins": "*"}})

#El cors nos sirve para dar permisos