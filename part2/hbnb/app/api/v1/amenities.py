from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'id': fields.String(readonly=True, description='The unique identifier of an amenity'),
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
    
})

def serialize_amenity(amenity):
    """Convert an Amenity object into a JSON-safe dictionary."""
    return {
        "id": amenity.id,
        "name": amenity.name,
        "description": amenity.description
    }

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')

    def post(self):

        """create a new amenity"""
        
        amenity_data = api.payload

        try:
            
            new_amenity = facade.create_amenity(amenity_data)
            return serialize_amenity(new_amenity), 201

        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }, 400

    @api.response(200, "List of amenities retrieved successfully")

    def get(self):
        """Get a list of all amenities."""
        amenities = facade.get_all_amenities()

        return [
            serialize_amenity(amenity)
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
@api.param(
    "amenity_id",
    "The unique identifier of the amenity"
)

class AmenityResource(Resource):
     """Resource for individual amenity operations."""

@api.response(200, 'Amenity details retrieved successfully')
@api.response(404, 'Amenity not found')

def get(self, amenity_id):
        
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404
        return serialize_amenity(amenity), 200

@api.expect(amenity_model, validate=True)
@api.response(200, 'Amenity updated successfully')
@api.response(404, 'Amenity not found')
@api.response(400, 'Invalid input data')

def put(self, amenity_id):
        """Update an amenity's information"""

        amenity = facade.get_amenity(amenity_id)

        if amenity is None:
            return {"error": "Amenity not found"}, 404

        amenity_data = api.payload

        try:
            facade.update_amenity(amenity_id, amenity_data)
            return {"message": "Amenity updated successfully"}, 200
        
        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }, 400
