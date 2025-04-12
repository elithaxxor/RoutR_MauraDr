from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

auth_ns = Namespace('auth', description='Authentication operations')

# Mock user database (replace with SQLite in production)
users = {'admin': generate_password_hash('password123')}

login_model = auth_ns.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = auth_ns.payload
        username = data.get('username')
        password = data.get('password')
        if username in users and check_password_hash(users[username], password):
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401
