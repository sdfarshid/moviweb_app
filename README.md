# MovieWebApp

### Overview

MovieWebApp is a web application that allows users to manage their favorite movies. Users can add movies, update movie information, delete movies, and view their movie lists. Additionally, the application includes API endpoints to handle movie and user data programmatically. This project is built using **Flask** and integrates with **SQLAlchemy** for database management.

---

## Technologies Used

- **Backend**: Flask (Python), Flask-SQLAlchemy
- **Database**: SQLite
- **Frontend**: Bootstrap 5


---

### Features

- **User Management**: Create, list, and manage users.
- **Movie Management**: Add, update, delete, and view movies for each user.
- **API Integration**: Expose movie-related functionalities through a RESTful API.
- **Database**: Stores user and movie information using **SQLite** with **SQLAlchemy** ORM.

---

## Project Structure

```plaintext
.
MovieWebApp/ │
.
├── app.py                         # Main application file
├── config.py                      # Configuration settings for the app
├── requirements.txt               # Python dependencies
├── routes/
│   ├── api.py                    # API route handlers
│   ├── movies.py                 # Movie-related routes
│   └── user.py                   # User-related routes
├── services/
│   ├── movie_service.py           # Logic for handling movie-related operations
│   └── user_service.py            # Logic for handling user-related operations
├── models/
│   ├── __init__.py                # Initializes the database and model relationships
│   ├── movie.py                   # Movie model
│   ├── user.py                    # User model
│   ├── user_movie.py              # Relationship model between users and movies
│   └── db.py                      # Database setup
└── tests/
    ├── test_app.py                # Web integration tests
    ├── test_data_manager.py       # Data_manager tests
    └── test_services.py           # Unit tests for services

```



### Setup

To get started with the MovieWebApp, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/MovieWebApp.git

2. **Install dependencies:**
Navigate to the project folder and install the required packages using pip.

   ```bash
   pip install -r requirements.txt


3. **Initialize the database:**
Ensure that the database is initialized and the required tables are created.

   ```bash
   python
   from app import app
   from models import init_db
   init_db(app)


4. **Initialize the database:**
   To start the development server:
   ```bash
   python app.py
------
Usage

**Web Interface**

* Home Page: / – Displays a list of movies with options for sorting and filtering.
* Users: /users/list – List all users.
* Add User: /users/add_user – Add a new user.
* User's Movies: /users/<int:user_id>/movies – View movies associated with a user.
* Add Movie to User: /users/<int:user_id>/add_movie – Add a movie to a user's list.
* Update Movie: /users/<int:user_id>/update_movie/<int:movie_id> – Update movie details for a user.
* Delete Movie: /users/<int:user_id>/delete_movie/<int:movie_id> – Remove a movie from a user's list.
 -----
**API Endpoints**
* GET /api/movies: Get a list of movies with pagination and sorting.
* POST /api/users/add: Add a new user.
* GET /api/users/list: List all users.
* GET /api/users/int:user_id/movies: Get a user's movie list.
* POST /api/users/int:user_id/add-user-movie: Add a movie to a user's list.
* PUT /api/users/int:user_id/update_movie/int:movie_id: Update movie details for a user.
* DELETE /api/users/int:user_id/delete/movie/int:movie_id: Delete a movie from a user's list.

----- 

**Error Handling**
* 404 Not Found: The requested resource could not be found.
* 405 Method Not Allowed: The method is not allowed for the requested URL.
* 400 Bad Request: The request is missing required data or has invalid data.
* 500 Internal Server Error: An unexpected error occurred on the server.

Testing
To test the application, we use unittest and Flask's test client. The tests are located in the test folder. You can run the tests using the following command:
