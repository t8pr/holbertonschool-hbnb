import email
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.models.booking import Booking

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.booking_repo = SQLAlchemyRepository(Booking)

    
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
    
    def delete_amenity(self, amenity_id):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return False
        self.amenity_repo.delete(amenity_id)
        return True

    
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
        
        
        amenities_list = place_data.get('amenities', [])
        for am_id in amenities_list:
            amenity = self.amenity_repo.get(am_id)
            if amenity:
                place.amenities.append(amenity)
                
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None
            
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities = [] 
            for am_id in amenity_ids:
                amenity = self.amenity_repo.get(am_id)
                if amenity:
                    place.amenities.append(amenity)
                    
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    
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
        
        
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id) 
        return True

    def delete_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return False
        self.place_repo.delete(place_id)
        return True

    def delete_user(self, user_id):
        user = self.user_repo.get(user_id)
        if not user:
            return False
        self.user_repo.delete(user_id)
        return True

    def create_booking(self, data):
        booking = Booking(**data)
        self.booking_repo.add(booking)
        return booking

    def get_bookings_by_user(self, user_id):
        return self.booking_repo.model.query.filter_by(user_id=user_id).all()

    def get_bookings_by_place(self, place_id):
        return self.booking_repo.model.query.filter_by(place_id=place_id).all()

    def toggle_favorite(self, user_id, place_id):
        user = self.user_repo.get(user_id)
        place = self.place_repo.get(place_id)
        if not user or not place:
            return False
            
        if place in user.favorites:
            user.favorites.remove(place)
            is_favorite = False
        else:
            user.favorites.append(place)
            is_favorite = True
            
        from app import db
        db.session.commit()
        return is_favorite

    def get_user_favorites(self, user_id):
        user = self.user_repo.get(user_id)
        return user.favorites if user else []