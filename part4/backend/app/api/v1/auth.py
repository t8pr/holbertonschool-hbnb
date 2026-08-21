from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

register_model = api.model('Register', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/register')
class Register(Resource):
    @api.expect(register_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered or invalid data')
    def post(self):
        """Register a new user"""
        user_data = api.payload
        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {"error": "Email already registered"}, 400
            
            new_user = facade.create_user(user_data)
            return {"id": new_user.id, "message": "User created successfully"}, 201
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
        

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Retrieve the user based on the provided email
        email = credentials['email']
        password = credentials['password']

        # find the user
        user = facade.get_user_by_email(email)
        
        # Check if the user exists and the password is correct
        if not user or not user.verify_password(password):
            return {'error': 'Invalid credentials'}, 401

        # Create a JWT including the is_admin claim
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'is_admin': user.is_admin}
        )
        
        # Return the JWT token to the user
        return {'access_token': access_token}, 200