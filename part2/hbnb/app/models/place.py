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
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    @property
    def owner(self):
        """Return a proxy object for the owner."""
        class OwnerProxy:
            def __init__(self, owner_id):
                self.id = owner_id
        return OwnerProxy(self.owner_id)