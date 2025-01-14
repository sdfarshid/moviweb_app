import unittest
from unittest.mock import MagicMock, patch
from exceptions.UserErrors import UserNotFoundError
from services.user_service import get_user, add_user_movie, delete_user_movie
from services.movie_service import proces_add_movie


class UserServiceUnitTest(unittest.TestCase):
    @patch('services.user_service.data_manager')
    def test_get_user_success(self, mock_data_manager):
        # Mock the data_manager to return a user with a specific name
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Test User"
        mock_data_manager.get_user_by_id.return_value = mock_user

        user = get_user(1)

        self.assertEqual(user.name, "Test User")
        self.assertEqual(user.id, 1)

    @patch('services.user_service.data_manager')
    def test_get_user_not_found(self, mock_data_manager):
        mock_data_manager.get_user_by_id.side_effect = UserNotFoundError("User not found.")
        with self.assertRaises(UserNotFoundError):
            get_user(999)

    @patch('services.user_service.data_manager')
    def test_delete_user_movie(self, mock_data_manager):
        # Mock the data_manager to simulate successful deletion
        mock_data_manager.delete_user_movie.return_value = {"status": True}
        result = delete_user_movie(1, 1)
        self.assertTrue(result)

    @patch('services.movie_service.add_new_movie_with_api')
    @patch('services.movie_service.data_manager')
    def test_proces_add_movie(self, mock_data_manager, mock_add_new_movie_with_api):
        mock_data_manager.get_movie_by_name.return_value = None
        mock_movie = MagicMock()
        mock_movie.id = 1
        mock_movie.name = "Test Movie"
        mock_add_new_movie_with_api.return_value = mock_movie

        movie = proces_add_movie("Test Movie")
        self.assertEqual(movie.name, "Test Movie")
        self.assertEqual(movie.id, 1)

    @patch('services.movie_service.add_new_movie_with_api')
    @patch('services.movie_service.data_manager.get_movie_by_name')
    def test_proces_add_movie_existing_movie(self, mock_get_movie_by_name, mock_add_new_movie_with_api):
        # Mocking get_movie_by_name to return an existing movie
        mock_movie = MagicMock()
        mock_movie.id = 1
        mock_movie.name = "Test Movie"
        mock_get_movie_by_name.return_value = mock_movie

        # Call proces_add_movie
        movie = proces_add_movie("Test Movie")

        # Assertions
        self.assertEqual(movie.id, 1)
        self.assertEqual(movie.name, "Test Movie")
        mock_get_movie_by_name.assert_called_once_with("Test Movie")
        mock_add_new_movie_with_api.assert_not_called()

    @patch('services.movie_service.add_new_movie_with_api')
    @patch('services.movie_service.data_manager.get_movie_by_name')
    def test_proces_add_movie_new_movie(self, mock_get_movie_by_name, mock_add_new_movie_with_api):
        # Mocking get_movie_by_name to return None
        mock_get_movie_by_name.return_value = None

        # Mocking add_new_movie_with_api to add a new movie
        mock_movie = MagicMock()
        mock_movie.id = 2
        mock_movie.name = "New Test Movie"
        mock_add_new_movie_with_api.return_value = mock_movie

        # Call proces_add_movie
        movie = proces_add_movie("New Test Movie")

        self.assertEqual(movie.id, 2)
        self.assertEqual(movie.name, "New Test Movie")
        mock_get_movie_by_name.assert_called_once_with("New Test Movie")
        mock_add_new_movie_with_api.assert_called_once_with("New Test Movie")

    @patch('services.movie_service.add_new_movie_with_api')
    @patch('services.movie_service.data_manager.get_movie_by_name')
    def test_proces_add_movie_failure(self, mock_get_movie_by_name, mock_add_new_movie_with_api):
        # Mocking get_movie_by_name to return None
        mock_get_movie_by_name.return_value = None

        # Mocking add_new_movie_with_api to raise an exception
        mock_add_new_movie_with_api.side_effect = ValueError("API Error")

        # Call proces_add_movie and expect an exception
        with self.assertRaises(ValueError) as context:
            proces_add_movie("Failing Movie")

        # Assertions
        self.assertIn("Have Error in API", str(context.exception))
        mock_get_movie_by_name.assert_called_once_with("Failing Movie")
        mock_add_new_movie_with_api.assert_called_once_with("Failing Movie")




if __name__ == "__main__":
    unittest.main()
