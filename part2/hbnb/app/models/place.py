from app.models.basemodel import BaseModel

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner_id):
        super().__init__()
        
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if price < 0:
            raise ValueError("Price must be a positive value")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
            
        self.title = title
        self.description = description
        self.price = float(price)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.owner_id = owner_id
        self._owner = None
        self.reviews = []
        self.amenities = []

    @property
    def owner(self):
        """Return the actual owner object if resolved, otherwise a proxy."""
        if self._owner:
            return self._owner
        
        class OwnerProxy:
            def __init__(self, owner_id):
                self.id = owner_id
                self.first_name = "Unknown"
                self.last_name = "User"
                self.email = "unknown@example.com"
        return OwnerProxy(self.owner_id)

    @owner.setter
    def owner(self, user_obj):
        """Allow setting the actual user object as the owner."""
        self._owner = user_obj
        if user_obj:
            self.owner_id = user_obj.id

    def to_dict(self, detailed=True):
        """Return a dictionary representation."""
        if not detailed:
            return {
                "id": self.id,
                "title": self.title,
                "latitude": self.latitude,
                "longitude": self.longitude
            }

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": {
                "id": self.owner.id,
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name,
                "email": self.owner.email
            },
            "amenities": [
                {
                    "id": amenity.id,
                    "name": amenity.name
                }
                for amenity in self.amenities
            ],
            "reviews": [
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating,
                    "user_id": review.user_id
                }
                for review in self.reviews
            ]
        }