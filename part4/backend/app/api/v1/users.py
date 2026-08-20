from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    """Resource for user list operations (Get, Post)"""

    @api.response(200, 'Users successfully retrieved')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [user.to_dict() for user in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user account with unique email """
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        try:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user:
                return {"error": "Email already registered"}, 400

            new_user = facade.create_user(user_data) 
            return {"id": new_user.id, "message": "User created successfully"}, 201
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400


@api.route('/<string:user_id>')
@api.param("user_id", "The unique identifier of the user")

class UserResource(Resource):
    """Resource for individual user operations"""

    @api.response(200, 'User successfully retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID"""
        user = facade.get_user(user_id)
        if not user:
             return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Bad Request')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update an existing user"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        if not is_admin and user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        user_data = api.payload
        if not user_data:
            return {"error": "No update data provided"}, 400

        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {'error': 'You cannot modify email or password.'}, 400

        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user and existing_user.id != user_id:
                return {"error": "Email already in use"}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {"error": "User not found"}, 404
            return updated_user.to_dict(), 200
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400
