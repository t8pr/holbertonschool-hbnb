#  Detailed Sequence Diagrams for API Calls


##  Contents
1. [Class Diagram](#class-diagram)
2. [Explanatory Notes](#explanatory-notes)
3. [Author](#author)



## Sequence Diagrams for API Calls

## Sequence Diagrams — Explanatory Notes

The sequence diagrams describe how the main API requests are processed inside the HBnB system. Each diagram focuses on one specific action, such as registering a user, creating a place, submitting a review, or fetching a list of places.

For each sequence, the document explains the purpose of the API call, the main steps involved, and how each layer contributes to completing the request.

---

![alt text](Seq-RegisterG11.svg)

## 1. User Registration Sequence

**API Call:**
`POST /api/v1/users`

**Purpose:**
This sequence explains how a new user account is created. It also shows how the system validates user data and prevents duplicate accounts by checking whether the email already exists.

**Flow of Interactions:**
The user sends registration data to the Presentation Layer. The API forwards the request to the Business Logic Layer, where the input is validated. The Business Logic Layer then communicates with the Persistence Layer to check if the email is already stored. If the email exists, an error response is returned. If not, the new user is saved, and the system returns a success response.

**Layer Contributions:**

* **Presentation Layer:** Receives the registration request and returns the final response.
* **Business Logic Layer:** Validates the input and decides whether the account can be created.
* **Persistence Layer:** Checks for existing users and stores the new user data.

---

## 2. Place Creation Sequence

![alt text](Seq-PlcaeCreationG11.svg)

**API Call:**
`POST /api/v1/places`

**Purpose:**
This sequence explains how an owner creates a new place listing. It also shows how the system checks authentication and validates the place information before saving it.

**Flow of Interactions:**
The owner sends place details to the Presentation Layer. The request is checked for authentication, usually through a token. After the user is verified, the Business Logic Layer validates the place data, such as title, price, location, and availability. If the data is valid, the Persistence Layer stores the new place. A success response is then returned to the owner.

**Layer Contributions:**

* **Presentation Layer:** Receives the place creation request and sends back the response.
* **Auth Layer:** Verifies that the user is authenticated and allowed to create a place.
* **Business Logic Layer:** Checks the place details and applies business rules.
* **Persistence Layer:** Saves the new place record in the database.

---

## 3. Review Submission Sequence

![alt text](Seq-ReviewSubmissionG11.svg)

**API Call:**
`POST /api/v1/reviews`

**Purpose:**
This sequence explains how a user submits a review for a place. It ensures that the user is authenticated and that the place being reviewed exists.

**Flow of Interactions:**
The user sends a review request containing a rating, comment, and place ID. The system first checks authentication. After that, the Business Logic Layer validates the review data and confirms that the target place exists by communicating with the Persistence Layer. If the place is found and the review is valid, the review is saved and a success response is returned.

**Layer Contributions:**

* **Presentation Layer:** Receives the review request and returns the result.
* **Auth Layer:** Confirms that the user is logged in.
* **Business Logic Layer:** Validates the rating, comment, and review rules.
* **Persistence Layer:** Checks the place record and saves the review.

---

## 4. Fetch Places Sequence

![alt text](Seq-Fetching_A_List_OF_PlaceG11.svg)

**API Call:**
`GET /api/v1/places?city=Riyadh`

**Purpose:**
This sequence explains how users retrieve a list of places based on filters, such as city, price, or availability.

**Flow of Interactions:**
The user sends a request to view places. The Presentation Layer receives the request and extracts any query parameters, such as `city=Riyadh`. The Business Logic Layer prepares the search criteria and passes them to the Persistence Layer. The database returns matching places, and the result is sent back to the user.

**Layer Contributions:**

* **Presentation Layer:** Receives the search request and returns the list of places.
* **Business Logic Layer:** Processes the filter criteria and prepares the search operation.
* **Persistence Layer:** Executes the database query and retrieves matching records.

---

## Authors
* **Abdulrhman Alsalhi** - [ARAlsalhi](https://github.com/ARAlsalhi)
