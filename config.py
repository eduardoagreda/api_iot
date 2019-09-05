import os

#Se necesita cambiar los datos de las variables username, password, hostname y db_name
DB_URI = "mysql+mysqldb://{username}:{password}@{hostname}/{db_name}".format(
    username="root", 
    password="", 
    hostname="localhost", 
    db_name="api_resi")

class Config(object):
    DEBUG = False
    TESTING = False
    #para generar la SECRET_KEY, se abre la consola de python y se importa la biblioteca secrets; posteriormente se genera con el comando secrets.token_urlsafe(16)
    SECRET_KEY = 'By0HXCzdvh9fpV95x1RTCg'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True