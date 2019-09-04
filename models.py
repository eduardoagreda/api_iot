#importación de módulos python (librerías)
from datetime import datetime
from app import db, ma

from sqlalchemy import BOOLEAN
from werkzeug.security import check_password_hash, generate_password_hash        
from flask_marshmallow import Schema, fields
from marshmallow import ValidationError

#creación de las clases para el diseño de modeles (creación de la base de datos)
class User(db.Model):
    #asignación al nombre de la tabla en la base de datos
    __tablename__ = 'users'

    #columnas de la tabla users
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    device = db.relationship('Device', backref='owner', lazy=True)

    #métodos para la creación del usuario, la contraseña, la verificación de contraseña y la forma de ver al usuario
    def __init__(self, name, last_name, username, email, password):
        self.name = name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.__create_password(password)
        
    def __create_password(self, password):
        return generate_password_hash(password)
            
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username

class Device(db.Model):
    #nombre de la tabla device
    __tablename__ = 'devices'
    
    #columnas que contiene la tabla devices
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False)
    ip_address = db.Column(db.String(15), nullable=False)
    mac_address = db.Column(db.String(17), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    samples = db.relationship('Sample', backref='device', lazy=True)
    relays = db.relationship('Relay', backref='device', lazy=True)

    def __init__(self, name, ip_address, mac_address, user_id):
        self.name = name
        self.ip_address = ip_address
        self.mac_address = mac_address
        self.user_id = user_id

    def __repr__(self):
        return '<Device %r>' % self.name

class Sample(db.Model):
    #nombre de la tabla sample
    __tablename__ = 'samples'

    #columnas que contiene la tabla samples
    id = db.Column(db.Integer, primary_key = True)
    analog1 = db.Column(db.Integer)
    analog2 = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.now)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)    

    def __init__(self, analog1, analog2, device_id):
        self.analog1 = analog1
        self.analog2 = analog2
        self.device_id = device_id

class Relay(db.Model):
    #nombre de la tabla relay
    __tablename__ = 'relays'

    #columnas que contiene la tabla relay
    id = id = db.Column(db.Integer, primary_key = True)
    log1 = db.Column(db.BOOLEAN, default=False, nullable=False)
    log2 = db.Column(db.BOOLEAN, default=False, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'), nullable=False)    

    def __init__(self, log1, log2, device_id):
        self.log1 = log1
        self.log2 = log2
        self.device_id = device_id

#Creación de los esquemas para que se serialicen las tablas creadas
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class DeviceSchema(ma.ModelSchema):
    class Meta:
        model = Device

class SampleSchema(ma.ModelSchema):
    class Meta:
        model = Sample

class RelaySchema(ma.ModelSchema):
    class Meta:
        model = Relay
