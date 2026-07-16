from app.models.basemodel import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required and max 50 chars")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required and max 50 chars")
        if not email:
            raise ValueError("Email is required")
            
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        """
        check with Eman 


        from app.models.basemodel import BaseModel


class User(BaseModel):
    """User model."""

    def __init__(
        self,
        first_name,
        last_name,
        email,
        is_admin=False
    ):
        super().__init__()

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    def to_dict(self):
        """Convert the user object to a dictionary."""
        user_data = self.__dict__.copy()

        if "created_at" in user_data:
            user_data["created_at"] = (
                user_data["created_at"].isoformat()
            )

        if "updated_at" in user_data:
            user_data["updated_at"] = (
                user_data["updated_at"].isoformat()
            )

        return user_data
        
        
        """
