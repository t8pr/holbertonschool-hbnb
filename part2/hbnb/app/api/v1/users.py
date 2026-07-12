from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'id': fields.String(readonly=True, description='The unique identifier of a user'),
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'BirthDate': fields.Integer(required=False, description='Birthdate of the user in YYYY-MM-DD format'),
    'isAdmin': fields.Boolean(required=False, description='Indicates if the user has admin privileges'),
    'phoneNum': fields.Integer(required=False, description='Phone number of the user'),
    'User_Rule': fields.String(required=True, enum=['user', 'owner'], description='Role of the user', example='user')
})

#  help function to serialize user data for responses (No need to repeat this part of code :) )
# it called Data Transfer Object (DTO) 

def serialize_user(user):
    """Convert a User object into a safe response dictionary."""

    birth_date = getattr(user, 'birth_date', None)

    if birth_date and hasattr(birth_date, 'isoformat'):
        birth_date = birth_date.isoformat()

    user_rule = getattr(user, 'user_rule', None)

    if user_rule and hasattr(user_rule, 'value'):
        user_rule = user_rule.value

    return {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'birth_date': birth_date,
        'is_admin': getattr(user, 'is_admin', False),
        'phone_num': getattr(user, 'phone_num', None),
        'user_rule': user_rule
    }

@api.route('/')
class UserList(Resource):
    """Resource for user list operations (Get, Post)"""

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):

        """Register a new user
        Create a new user account with unique email.
        Returns the created user details with assigned ID if successful,
        or an error message if the email is already registered or input data is invalid.
        
        """
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)

        existing_user = facade.get_user_by_email(user_data['email'])

        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return serialize_user(new_user), 201
        
        except (ValueError, TypeError) as error:
            return {'error': str(error)}, 400

@api.response(200, 'Users successfully retrieved')
def get(self):
        """Get all users"""
        users = facade.get_all_users()

        return [
            serialize_user(user)
            for user in users
        ], 200
        
     # Get and Put methods for individual user operations (Get, Put)
     
@api.route('/<string:user_id>')
class UserResource(Resource):
    """Resource for individual user operations."""

    @api.response(200, 'User successfully retrieved')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Retrieve a user by ID."""
        user = facade.get_user(user_id)

        if user is None:
            return {
                'error': 'User not found'
            }, 404

        return serialize_user(user), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User not found')

    def put(self, user_id):
        """Update an existing user."""
        user = facade.get_user(user_id)

        if user is None:
            return {
                'error': 'User not found'
            }, 404

        user_data = api.payload

        existing_user = facade.get_user_by_email(
            user_data['email']
        )

        if (
            existing_user is not None
            and existing_user.id != user_id
        ):
            return {
                'error': 'Email already registered'
            }, 400

        try:
            updated_user = facade.update_user(
                user_id,
                user_data
            )

            return serialize_user(updated_user), 200

        except (ValueError, TypeError) as error:
            return {
                'error': str(error)
            }, 400
