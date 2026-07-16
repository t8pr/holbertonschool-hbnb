from app.models.basemodel import BaseModel

class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()
        
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
            
        self.name = name
        self.description = description


        """
        def to_dict(self):
        """Convert the amenity object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name
        }
        
        """
