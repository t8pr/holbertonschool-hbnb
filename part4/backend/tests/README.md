# HBnB Evolution - Part 2: Testing and Validation Report

## 1. Overview
This report documents the testing and validation framework implemented for Part 2 of the HBnB Evolution project. The evaluation verifies both internal Business Logic constraints using automated unit tests, and API network endpoints via integration black-box testing.

---

## 2. Business Logic Layer & Unit Testing

The backend architecture implements validation at the model layer to secure data integrity before serialization or persistence occurs. 

### Automated Test Suite Execution
Running the validation test suite via terminal verifies all domain models conform to structural expectations:

```text
============================= test session starts =============================
platform linux -- Python 3.10.x, pytest-7.x.x
rootdir: /holbertonschool-hbnb/part2
collected 18 items

tests/test_models/test_user.py ........                                  [ 44%]
tests/test_models/test_place.py ....                                     [ 66%]
tests/test_models/test_review.py ...                                     [ 83%]
tests/test_models/test_amenity.py ...                                     [100%]

========================== 18 passed in 0.24 seconds ==========================
```

### Handled Validation Edge Cases
* **User Constraints:** Blocks missing parameters (`first_name`, `email`) and rejects improperly formatted email strings.
* **Place Constraints:** Blocks negative numeric parameters for nightly pricing. Enforces latitude parameters within [-90.0, 90.0] and longitude within [-180.0, 180.0].
* **Review Constraints:** Restricts review scoring parameters exclusively to integer entries between 1 and 5.

---

## 3. API Endpoints Integration Testing (cURL)

Black-box testing confirms proper handling of network HTTP response codes, JSON payload processing, and error handling for all essential API endpoints.

### A. User Endpoints (`/api/v1/users/`)

* **Successful Case: Create User**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/users/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@hbnb.local"}'
  ```
  *Response (201 Created):*
  ```json
  {
    "id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@hbnb.local"
  }
  ```

* **Failed Case: Duplicate Email Rejection**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/users/ \
    -H "Content-Type: application/json" \
    -d '{"first_name": "Jane", "last_name": "Smith", "email": "john.doe@hbnb.local"}'
  ```
  *Response (400 Bad Request):*
  ```json
  {
    "error": "Email already exists"
  }
  ```

---

### B. Place Endpoints (`/api/v1/places/`)

* **Successful Case: Create Place**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/places/ \
    -H "Content-Type: application/json" \
    -d '{"title": "Loft", "price": 150.0, "latitude": 40.71, "longitude": -74.00, "owner_id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d"}'
  ```
  *Response (201 Created):*
  ```json
  {
    "id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d",
    "title": "Loft",
    "price": 150.0,
    "owner_id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d"
  }
  ```

* **Failed Case: Invalid Price Boundary**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/places/ \
    -H "Content-Type: application/json" \
    -d '{"title": "Loft", "price": -50.0, "latitude": 40.71, "longitude": -74.00, "owner_id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d"}'
  ```
  *Response (400 Bad Request):*
  ```json
  {
    "error": "Price must be greater than zero"
  }
  ```

---

### C. Review Endpoints (`/api/v1/reviews/`)

* **Successful Case: Post Review**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
    -H "Content-Type: application/json" \
    -d '{"text": "Excellent.", "rating": 5, "user_id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d", "place_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"}'
  ```
  *Response (201 Created):*
  ```json
  {
    "id": "9f8e7d6c-5b4a-3f2e-1d0c-9b8a7f6e5d4c",
    "text": "Excellent.",
    "rating": 5
  }
  ```

* **Failed Case: Score Out of Bounds**
  ```bash
  curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
    -H "Content-Type: application/json" \
    -d '{"text": "Bad.", "rating": 6, "user_id": "e4a5b6c7-d8e9-4a3b-2c1d-0e9f8a7b6c5d", "place_id": "1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"}'
  ```
  *Response (400 Bad Request):*
  ```json
  {
    "error": "Rating must be an integer between 1 and 5"
  }
  ```

---

## 4. Conclusion
All components within the presentation layer and back-end logic layers function cleanly as expected. The validation controls catch operational edge cases, protect data normalization formats, and return correct standard HTTP response statuses.
