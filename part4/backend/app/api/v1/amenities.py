"""Amenity API endpoints"""
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace("amenities", description="Amenity operations")

amenity_model = api.model("Amenity", {
    "name": fields.String(required=True, description="Name of the amenity"),
    "description": fields.String(required=False, description="Description of the amenity")
})

@api.route("/")
class AmenityList(Resource):
    @api.response(200, "List of amenities retrieved successfully")
    def get(self):
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity successfully created")
    @jwt_required()
    def post(self):
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

@api.route("/<string:amenity_id>")
@api.param("amenity_id", "The unique identifier of the amenity")
class AmenityResource(Resource):
    @api.response(200, "Amenity successfully retrieved")
    @api.response(404, "Amenity not found")
    def get(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity successfully updated")
    @jwt_required()
    def put(self, amenity_id):
        amenity_data = api.payload
        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {"error": "Amenity not found"}, 404
            return updated_amenity.to_dict(), 200
        except (ValueError, TypeError) as error:
            return {"error": str(error)}, 400

    @api.response(200, "Amenity successfully deleted")
    @api.response(404, "Amenity not found")
    @jwt_required()
    def delete(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        facade.delete_amenity(amenity_id)
        return {"message": "Amenity deleted successfully"}, 200