import email
from part4.backend.hbnb.app.persistence.repository import SQLAlchemyRepository
from part4.backend.hbnb.app.persistence.user_repository import UserRepository
from part4.backend.hbnb.app.models.user import User
from part4.backend.hbnb.app.models.amenity import Amenity
from part4.backend.hbnb.app.models.place import Place
from part4.backend.hbnb.app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # --- USER OPERATIONS ---
    def create_user(self, user_data):
        clean_data = {
            'first_name': user_data.get('first_name'),
            'last_name': user_data.get('last_name'),
            'email': user_data.get('email'),
            'password': user_data.get('password')
        }
        
        user = User(**clean_data)
        existing_user = self.get_user_by_email(user.email)
        if existing_user:
            raise ValueError("Email already registered")
            
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        if not isinstance(email, str):
            return None
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None
            
        allowed_fields = {"first_name", "last_name", "email"}
        clean_data = {key: value for key, value in user_data.items()
                      if key in allowed_fields}
                      
        if "email" in clean_data:
            new_email = clean_data["email"]
            if isinstance(new_email, str):
                new_email = new_email
                clean_data["email"] = new_email
                
            existing_user = self.get_user_by_email(new_email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("Email already registered")
                
        self.user_repo.update(user_id, clean_data)
        return self.user_repo.get(user_id)

    # --- AMENITY OPERATIONS ---
    def create_amenity(self, amenity_data):
        clean_data = {
            'name': amenity_data.get('name'),
            'description': amenity_data.get('description', '')
        }
        amenity = Amenity(**clean_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # --- PLACE OPERATIONS ---
    def create_place(self, place_data):
        clean_data = {
            'title': place_data.get('title'),
            'description': place_data.get('description', ''),
            'price': float(place_data.get('price')),
            'latitude': float(place_data.get('latitude')),
            'longitude': float(place_data.get('longitude')),
            'owner_id': place_data.get('owner_id')
        }
        place = Place(**clean_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # --- REVIEW OPERATIONS ---
    def create_review(self, review_data):
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        return [r for r in self.review_repo.get_all() 
                if r.place_id == place_id]

    def update_review(self, review_id, review_data):
        self.review_repo.update(review_id, review_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        # we need to handle the case where the review does not exist
        
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id) 
        return True
