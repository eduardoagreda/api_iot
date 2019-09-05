from flask_restful import Resource
from app import app, api, db, auth, cross_origin #, users
from flask import request, jsonify, session
from models import User, UserSchema, Device, DeviceSchema, Sample, SampleSchema, Relay, RelaySchema

#Inicializamos los Schema, para el manejo de datos tipo json
user_schema = UserSchema()
device_schema = DeviceSchema()
sample_schema = SampleSchema()
relay_schema = RelaySchema()

#creamos las vistas basadas en clases para el envío y consulta de listas de datos
class Index(Resource):
    def get(self):
        result = 'Hello, %s!' %auth.username
        message = {'result':result}
        return jsonify(message)

class UserList(Resource):
    #decorators = [auth.login_required]
    def get(self):
        all_user = User.query.all()
        if all_user:
            message = user_schema.dump(all_user, many=True)
        else:
            message = {'result': 'No hay usuarios en la base de datos'}
        return jsonify(message)

    def post(self):
        data = request.get_json()
        name = data['name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']

        user = User.query.filter_by(username=username).first()
        email_user = User.query.filter_by(email=email).first()

        if user or email_user:
            message = {'data': 'El username %s ' % username + 'o el email %s' %email +' ya están agregados'}
        else:
            user_data = User(name=name, last_name=last_name, username=username, email=email, password=password)
            db.session.add(user_data)
            db.session.commit()
            message = {'data': 'success'}
        return jsonify(message)

class DeviceList(Resource):
    def get(self):
        all_device = Device.query.all()
        if all_device:
            result = device_schema.dump(all_device, many=True)
            message = {'result': result}
        else: 
            result = 'No hay dispositivos en la base de datos'
            message = {'result': result}
        return jsonify(message)

    def post(self):
        data = request.get_json()
        name = data['name']
        ip_address = data['ip_address']
        mac_address = data['mac_address']
        user_id = data['user_id']

        mac = Device.query.filter_by(mac_address=mac_address).first()

        if mac:
            result = 'La dirección Mac %s' % mac_address + ' ya está agregada.'
            message = {'result': result}
        else:
            device_data = Device(name=name, ip_address=ip_address, mac_address=mac_address, user_id=user_id)
            db.session.add(device_data)
            db.session.commit()
            result = 'Dispositivo añadido'
            message = {'result': result}
        return jsonify(message)

class SampleList(Resource):
    def get(self):
        all_sample = Sample.query.all()
        if all_sample:
            result = sample_schema.dump(all_sample, many=True)
            message = {'result': result}
        else:
            result = 'No hay datos en la base de datos'
            message = {'result': result}
        return jsonify(message)
    
    def post(self):
        data = request.get_json()
        analog1 = data['analog1']
        analog2 = data['analog2']
        device_id = data['device_id']

        sample = Sample.query.filter_by(device_id=device_id)

        if sample:
            result = 'No se han podido guardar los datos'
            message = {'result':result}
        else:
            sample_data = Sample(analog1=analog1, analog2=analog2, device_id=device_id)
            db.session.add(sample_data)
            db.session.commit()
            result = 'Datos registrados'
            message = {'result': result}
        return jsonify(message)

class RelayList(Resource):
    def get(self):
        all_relay = Relay.query.all()
        if all_relay:
            result = relay_schema.dump(all_relay, many=True)
            message = {'result': result}
        else:
            result = 'No hay datos en la base de datos'
            message = {'result': result}
        return jsonify(message)
    
    def post(self):
        data = request.get_json()
        log1 = data['log1']
        log2 = data['log2']
        device_id = data['device_id']

        relay = Relay.query.filter_by(device_id=device_id)

        if relay is None:
            result = 'No se han podido guardar los datos'
            message = {'result':result}
        else:
            relay_data = Relay(log1=log1, log2=log2, device_id=device_id)
            db.session.add(relay_data)
            db.session.commit()
            result = 'Datos añadidos'
            message = {'result': result}
        return jsonify(message)            

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user is not None and user.verify_password(password):
            result = "Bienvenido {}".format(username)
            message = {'result': result}
        else:
            result = "Datos incorrectos"
            message =  {'result': result}
        return jsonify(message)

#Creación de las búsquedas por medio de ID con vistas basadas en clases
class UserSearchID(Resource):
    def get(self, user_id):
        user_id = User.query.get(user_id)
        if user_id:
            result = user_schema.dump(user_id)
            message = {'result': result}
        else:
            result = 'El usuario no existe en nuestro sistema'
            message = {'result':result}
        return jsonify(message)

class DeviceSearchID(Resource):
    def get(self, device_id):
        device_id = Device.query.get(device_id)
        if device_id:
            result = device_schema.dump(device_id)
            message = {'result': result}
        else:
            result = 'El dispositivo no existe en nuestro sistema'
            message = {'result':result}
        return jsonify(message)

class SampleSearchID(Resource):
    def get(self, sample_id):
        sample_id = Sample.query.get(sample_id)
        if sample_id:
            result = device_schema.dump(sample_id)
            message = {'result': result}
        else:
            result = 'La muestra no existe en nuestro sistema'
            message = {'result':result}
        return jsonify(message)

class RelaySearchID(Resource):
    def get(self, relay_id):
        relay_id = Sample.query.get(relay_id)
        if relay_id:
            result = relay_schema.dump(relay_id)
            message = {'result': result}
        else:
            result = 'La dispositivo no existe en nuestro sistema'
            message = {'result':result}
        return jsonify(message)

#Creación de búsquedas por medio de Nombres, esto es para usuarios o dispositivos

#creamos las api's para obtener las direcciones url
api.add_resource(Index, '/api/index', endpoint='index')
api.add_resource(UserList, '/api/users', endpoint='users')
api.add_resource(DeviceList, '/api/devices', endpoint='devices')
api.add_resource(SampleList, '/api/sample', endpoint='sample')
api.add_resource(RelayList, '/api/relay', endpoint='relay')
api.add_resource(UserSearchID, '/api/<int:user_id>/user', endpoint='search_userID')
api.add_resource(DeviceSearchID, '/api/<int:device_id>/device', endpoint='search_deviceID')
api.add_resource(SampleSearchID, '/api/<int:sample_id>/sample', endpoint='search_sampleID')
api.add_resource(RelaySearchID, '/api/<int:relay_id>/relay', endpoint='search_relayID')
api.add_resource(Login, '/api/login', endpoint='login')

#inicializar servidor
if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(port=80, host='0.0.0.0')