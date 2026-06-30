# Detailed High-level Package Diagram

## Contents
- [High-levelPackage Diagram](#High-level-Package-Diagram)
- [Explanatory Notes](#explanatory-notes)
- [Layer Responsibilities](#layer-responsibilities)
- [Facade Pattern](#facade-pattern)
- [Communication Flow](#communication-flow)
- [Author](#author)

---

## High-level Package Diagram
![alt text](Hbnb_High_Level_Package_Diagram.svg)
---

## Explanatory notes

- The HBnB application follows a three-layer architecture to separate responsibilities and improve maintainability.
- Presentation Layer: Receives user requests through the API and services, then forwards them to the Facade.
- Business Logic Layer: Contains the core business logic and manages the main entities (User, Place, Review, and Amenity).
- Persistence Layer: Handles data storage and retrieval through repositories and the database.
- The Facade Pattern provides a single entry point between the Presentation Layer and the Business Logic Layer, reducing coupling and simplifying communication.
- Requests flow from the Presentation Layer → Business Logic Layer → Persistence Layer, and the response follows the same path back to the user.

---

## Layer Responsibilities

### Presentation Layer
- Handles user requests through APIs and services.
- Forwards requests to the Facade.
- Returns responses to the client.

### Business Logic Layer
- Contains the application's core business rules.
- Manages the User, Place, Review, and Amenity models.
- Coordinates operations with the Persistence Layer.

### Persistence Layer
- Handles data storage and retrieval.
- Uses repositories to communicate with the database.

---

## Facade Pattern

- Provides a single entry point to the Business Logic Layer.
- Simplifies communication between layers.
- Reduces coupling and hides implementation details.

---

## Communication Flow

1. Client sends a request to the Presentation Layer.
2. The Presentation Layer forwards the request to the Facade.
3. The Facade invokes the appropriate business model.
4. The Business Logic Layer accesses the Persistence Layer.
5. The database returns the result.
6. The response is returned to the client.

---

## Author
* **Eman Hamdan** - [iEmanHamdan](https://github.com/iEmanHamdan)
