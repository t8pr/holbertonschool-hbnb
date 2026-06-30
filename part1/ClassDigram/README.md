# Detailed Class Diagram for Business Logic Layer

## Contents
* [Class Diagram](#class-diagram)
* [Explanatory Notes](#explanatory-notes)
  * [Key Entities Breakdown](#key-entities-breakdown)
  * [Relationships Logic](#relationships-logic)
* [Author](#author)

---

## Class Diagram

![alt text](Hbnb_Class_Diagram.svg)

---

## Explanatory Notes

The domain model represents the main objects used inside the HBnB application. These objects describe the core data of the system, their internal behaviors, and how each part is connected to the others. The model is designed to keep each entity focused on a single responsibility, adhering to clean architecture principles.

### Key Entities Breakdown

The primary domain entities and their core responsibilities are:

* **User**: Represents individuals interacting with the system. It handles authentication (`Auth()`), registration, profile management, and tracks role permissions. It stores personal account information (`FirstName`, `LastName`, `Email`, `Password`, `BirthDate`, `PhoneNum`) and metadata (`Id` as UUID, `Create_date`, `Update_date`).
* **Place**: Represents a rental property listed in the system. It stores core property details (`Title`, `Description`, `Price`, `latitude`, `Longitude`) and an `Availability` boolean. It provides standard CRUD operations.
* **Review**: Captures user feedback through a `Rating` (Float) and a `Comment` (String). Like other entities, it is tracked via a UUID and timestamps.
* **Amenities**: A lookup entity representing features or services available in a place (`Name`, `Description`). Because amenities (e.g., Wi-Fi, pool) are shared across the platform, they are managed independently to prevent data duplication.
* **Favorite**: Operates as an association class between `User` and `Place`. It contains an `isFavorite` boolean and a method to `Create_favorite()`, cleanly linking users with places they want to bookmark.

**Core Business Rules:**
1. A user must have a unique email and their password must be handled securely.
2. Roles dictate permissions: A normal user (`USER`) browses and reviews; an owner (`OWNER`) can also manage their own places; an administrator (`ADMIN`) has global permissions. *(Note: The system is transitioning from boolean flags like `isAdmin` to a `UserRole` Enum for scalable role management).*
3. Ratings must fall within an allowed floating-point range. Empty or invalid string data for critical fields is rejected.

### Relationships Logic

The entities are connected through explicit cardinality to ensure data integrity and define system workflows:

* **User (1) → (0..*) Place**: A single user can own zero or multiple places. However, a specific place record belongs to only one user (the owner). A `Place` cannot exist without a valid `User`.
* **User (1) → (0..1) Review**: A user can leave up to one review per specific place context.
* **Place (0..1) → (0..*) Review**: A place can exist without reviews, but can accumulate many reviews over time. A `Review` requires both a valid `User` and a valid `Place`.
* **Place (*..1) → (1..*) Amenities**: A Many-to-Many relationship. A place must have at least one amenity, and an amenity can belong to many places. This allows for a centralized master list of amenities that owners select from.
* **User (1) ↔ (0..*) Place (via Favorite)**: A user can favorite many places. This is mapped through the Favorite association class to ensure a user cannot save the same `Place` to their list more than once, making database querying highly efficient.

---

## Author

Osama Alhamdan