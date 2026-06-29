# HBnB Technical Documentation

## 1. Introduction

HBnB is a simple rental platform inspired by Airbnb. It allows users to create places, add amenities, write reviews, save favorite places, and manage user information.

This document explains the main design of the HBnB application before coding. It gives a clear overview of the system structure, main parts, relationships, and layers.

The purpose of this document is to help developers understand how the application should be built in an organized and easy-to-maintain way.

---

## 2. System Overview

The HBnB application is designed to manage the basic features of a rental platform. Users can register, update their profile, create places, write reviews, add amenities, and save places as favorites.

The system also supports different user roles. Instead of using many Boolean attributes such as `isAdmin` and `isOwner`, the system uses a `UserRole` enum. This makes the design cleaner and easier to maintain.

The application is divided into layers. Each layer has a clear responsibility, which helps keep the project organized and easier to update later.

---

## 3. System Architecture and Package Design

The HBnB system follows a layered architecture. This means the system is separated into different parts, and each part has a specific job.

The main layers are:

* Presentation Layer
* Business Logic Layer
* Persistence Layer
* Core Entities

### 3.1 Presentation Layer

The Presentation Layer is responsible for receiving user requests and returning responses. In this project, it is represented by the API.

Its main responsibilities are:

* Receive requests from users
* Send requests to the Business Logic Layer
* Return success or error responses
* Handle request and response formatting

This layer does not contain the main business rules. Its role is mainly to connect the user with the system logic.

### 3.2 Business Logic Layer

The Business Logic Layer contains the main rules of the HBnB application. It manages the core operations related to users, places, reviews, amenities, and favorites.

Its main responsibilities are:

* Validate user input
* Apply business rules
* Manage user roles and permissions
* Control how entities interact with each other
* Decide when data should be created, updated, deleted, or retrieved

This layer is important because it controls how the application behaves.

### 3.3 Persistence Layer

The Persistence Layer is responsible for storing and retrieving data. It communicates with the database and keeps the data management separate from the rest of the system.

Its main responsibilities are:

* Save new records
* Retrieve existing records
* Update stored data
* Delete data
* Manage database communication

This separation makes the system cleaner because the Business Logic Layer does not need to directly handle database details.

### 3.4 Core Entities Package

The Core Entities package contains the main classes used in the HBnB application.

The main entities are:

* User
* UserRole
* Place
* Review
* Amenity
* Favorite

These entities represent the main objects in the system and define their attributes, methods, and relationships.

---

## 4. Domain Model Design

The domain model represents the main objects used inside the HBnB application. These objects describe the core data of the system and how each part is connected to the others.

The main domain entities are:

* User
* UserRole
* Place
* Review
* Amenity
* Favorite

Each entity has a clear responsibility. This helps keep the system organized and makes the application easier to understand, update, and maintain.

### 4.1 Main Domain Entities

| Entity   | Description                                           | Main Responsibility                                                                 |
| -------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------- |
| User     | Represents a person using the system.                 | Handles user information, authentication, profile updates, and user activity.       |
| UserRole | Defines the permission level of a user.               | Controls whether the user is a normal user, owner                       |
| Place    | Represents a rental place listed in the system.       | Stores place details such as title, description, price, location, and availability. |
| Review   | Represents feedback written by a user about a place.  | Stores ratings and comments linked to users and places.                             |
| Amenity  | Represents a feature or service available in a place. | Stores services such as Wi-Fi, parking, kitchen, or air conditioning.               |
| Favorite | Represents a saved place.                             | Connects users with places they want to save for later.                             |

### 4.2 User Role Design

The system uses a `UserRole` enum instead of multiple Boolean attributes such as`isOwner`, or `isUser`. Using an enum also makes the system easier to expand later. For example, new roles such as `MODERATOR` or `SUPPORT` can be added without changing the whole user structure.

This is a cleaner design because each user has one clear role.

The available roles are:

* `USER`: A normal user who can browse places, write reviews, and save favorite places.
* `OWNER`: A Normal user who can also create and manage their own places.
* `ADMIN`: A user with higher permissions who can manage users, places, reviews, and amenities.


### 4.3 Entity Responsibilities

The `User` entity stores personal account information and role data. It is responsible for registration, authentication, profile updates, and user-related actions.

The `Place` entity stores the information of rental places. Each place has an owner, location, price, availability status, and related amenities or reviews.

The `Review` entity stores user feedback. Each review must belong to one user and one place.

The `Amenity` entity stores available features that can be linked to places. A place can have many amenities, and the same amenity can be used by many places.

The `Favorite` entity connects users with places they want to save. It works as a link between the User and Place entities.

### 4.4 Design Rationale

The domain model is designed to keep each entity focused on one main purpose.

The User entity does not need an `isUser` attribute because every object created from the User class is already a user. Also, instead of using `isAdmin` and `isOwner`, the system uses `UserRole` to avoid confusion and make permissions easier to manage.

The Favorite entity is treated as a separate entity because it represents a relationship between a user and a place. This makes it easier to prevent duplicate favorites and to list saved places for each user.

The Amenity entity is separated from Place because the same amenity can be used by many places. This avoids repeated data and keeps the design cleaner.

### 4.5 Domain Model Summary

The domain model creates a clear structure for the HBnB application. Users can own places, write reviews, save favorites, and interact with amenities. Places can have reviews, amenities, and favorite records. Roles are managed through the UserRole enum to keep permissions simple and professional.

This design supports the main features of the system while keeping the application flexible for future changes.

---

## 5. Entity Relationships

The entities in the HBnB system are connected to each other through clear relationships.

The main relationships are:

* User 1 → 0..* Place
* User 1 → 0..* Review
* Place 1 → 0..* Review
* Place 0..* → 1..* Amenity
* User 1 → 0..* Favorite
* Place 1 → 0..* Favorite
* User → UserRole

### Relationship Explanation

A user can own many places.
A place belongs to one user.

A user can write many reviews.
A review belongs to one user.

A place can have many reviews.
A review belongs to one place.

A place can have many amenities.
An amenity can be linked to many places.

A user can save many favorite places.
A place can be saved by many users.

The Favorite entity works as a connection between User and Place.

The UserRole enum is used by the User entity to define the user’s permission level.

---

## 6. Business Rules

The HBnB system follows clear business rules to keep the data correct, safe, and organized.

The main business rules are:

* A user must have a unique email.
* A user must have one role from the UserRole enum.
* A normal user can browse places, write reviews, and save favorites.
* An owner can create and manage their own places.
* An admin can manage users, places, reviews, and amenities.
* A place must belong to an existing user.
* A review must belong to an existing user and an existing place.
* A rating should be within the allowed range.
* An amenity can be linked to one or more places.
* A favorite must connect one user with one place.
* A user should not save the same place as favorite more than once.
* Empty or invalid data should not be accepted.
* Sensitive actions, such as deleting users, should require admin permission.

---

## 7. Sequence Diagrams

The sequence diagrams describe how the main actions happen inside the HBnB system. They show how the user, Presentation Layer, Business Logic Layer, and Database interact step by step.

These diagrams are important because they explain the flow of requests before implementation. They also help developers understand which layer is responsible for each action.

---

## 7.1 User Registration Sequence Diagram

The user registration sequence explains how a new user creates an account in the HBnB application.

### 7.1.1 Data Flow and Interactions

1- User → Presentation Layer API:
The new user enters registration information such as first name, last name, email, password, birth date, and phone number.

2- Presentation Layer API → Business Logic Layer:
The API sends the user data to the Business Logic Layer using a registration request.

3- Business Logic Layer → Business Logic Layer:
The system validates the user data. It checks that all required fields are filled, the email format is valid, the password is acceptable, and the email is not already used by another account.

4- Business Logic Layer → Persistence Layer / Database:
If the validation is successful, the Business Logic Layer sends the new user data to the database to be stored.

5- Database → Business Logic Layer:
The database confirms that the new user was saved successfully.

6- Business Logic Layer → Presentation Layer API:
The Business Logic Layer returns an account creation confirmation to the API.

7- Presentation Layer API → User:
The API displays a success message to the user, such as “Account created successfully.”

### 7.1.2 Explanatory Notes

1- Purpose of the Diagram:
This diagram explains how a new user registers in the HBnB system. It also shows how the system checks user data before creating the account.

2- Key Components Involved:

* User
* Presentation Layer API
* Business Logic Layer
* Persistence Layer / Database

3- Design Decisions and Rationale:

* User input is validated before being saved.
* The email must be unique to prevent duplicate accounts.
* The API does not directly communicate with the database.
* The Business Logic Layer controls validation and account creation.
* The database is only used after the data passes validation.

4- Alternative Flow:

If the email already exists or the user data is invalid, the system does not create the account. Instead, the Business Logic Layer returns an error message to the API, and the API shows the error to the user.

Example errors:

* “Email already exists.”
* “Missing required fields.”
* “Invalid email format.”
* “Password is too weak.”

5- How It Fits into the Overall Architecture:
This sequence represents the first entry point for users in the HBnB system. It ensures that only valid and unique users are created. It also shows the responsibility of each layer clearly: the API receives the request, the Business Logic Layer applies the rules, and the database stores the final data.

---

## 8. Class Diagram Notes

The class diagram shows the main static structure of the HBnB system. It describes the classes, their attributes, methods, and relationships.

### 8.1 User Class Design

The User class should use:

* Role: UserRole

Instead of:

* isAdmin: Boolean
* isOwner: Boolean
* isUser: Boolean

This is more professional because the role is handled in one clear attribute. Also, `isUser` is not needed because every object created from the User class is already a user.

### 8.2 Favorite Class Design

The Favorite class should be treated as an entity that connects User and Place.

A better design for Favorite is:

* Id: UUID
* Create_date: Datetime

Main methods:

* Create_favorite()
* Delete_favorite()
* List_favorites()

The `isFavorite` attribute is optional and can be removed if the existence of the Favorite record already means the place is saved.

### 8.3 Naming Improvements

For a more professional UML diagram, class names should use singular form and start with a capital letter.

Recommended changes:

* favorite → Favorite
* Amenities → Amenity
* DataBase → Database
* presentionLayer → Presentation Layer
* Secces → Success
* displaySeccesMassage → displaySuccessMessage

---

## 9. Conclusion

This document explains the main design of the HBnB application. It describes the system architecture, package design, main entities, relationships, user roles, favorite feature, business rules, and sequence diagram flow.

The document will be used as a guide during implementation. It helps developers build the application in a clean, organized, and maintainable way.
