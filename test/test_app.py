import unittest
from app import app
from models import db
from models.user import User
from models.movie import Movie


class MovieWebIntegrationTest(unittest.TestCase):
    def setUp(self):
        # Setup Flask test client
        self.app = app.test_client()
        self.app.testing = True

        # Setup an in-memory SQLite database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['TESTING'] = True

        # Create the application context
        self.app_context = app.app_context()
        self.app_context.push()

        # Initialize the database
        db.create_all()

        # Add sample data
        user = User(name="Test User")
        movie = Movie(name="Test Movie", director="Test Director", year=2022, rating=8.5)
        db.session.add(user)
        db.session.add(movie)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_list_user(self):
        response = self.app.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Users List", response.data)

    def test_add_user(self):
        response = self.app.post('/add_user', data={"name": "New User"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"added successfully", response.data)

    def test_add_movie(self):
        response = self.app.post('/users/1/add_movie', data={"name": "New Movie"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"add", response.data)

    def test_delete_movie(self):
        self.app.post('/users/1/add_movie', data={"name": "New Movie"}, follow_redirects=True)
        # Then delete the movie
        response = self.app.get('/users/1/delete_movie/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Movie deleted successfully", response.data)

    def test_404_error(self):
        response = self.app.get('/non_existing_page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)


if __name__ == "__main__":
    unittest.main()
