import unittest
from unittest.mock import MagicMock
from data_manager.sqlite_data_manager import SQLiteDataManager
from exceptions.UserErrors import UserNotFoundError
from app import app
from models.user import User


class SQLiteDataManagerUnitTest(unittest.TestCase):
    def setUp(self):
        self.data_manager = SQLiteDataManager()
        self.data_manager.db = MagicMock()

        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()


    def test_get_user_by_id_success(self):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Test User"

        User.query = MagicMock()
        User.query.get.return_value = mock_user

        user = self.data_manager.get_user_by_id(1)

        self.assertEqual(user.id, 1)
        self.assertEqual(user.name, "Test User")

    def test_get_user_by_id_not_found(self):
        self.data_manager.db.session.query().get.return_value = None
        with self.assertRaises(UserNotFoundError):
            self.data_manager.get_user_by_id(999)

    def test_add_user_success(self):
        self.data_manager._commit_model_query = MagicMock()
        self.data_manager.add_user({"name": "Test User"})
        self.data_manager._commit_model_query.assert_called()


    def test_add_user_failure(self):
        self.data_manager._commit_model_query = MagicMock(side_effect=Exception("DB Error"))
        result = self.data_manager.add_user({"name": "Test User"})

        self.assertFalse(result["status"])
        self.assertIn("Error", result["message"])



    def test_delete_movie_success(self):
        mock_movie = MagicMock(id=1, name="Test Movie")
        self.data_manager.get_movie_by_id = MagicMock(return_value=mock_movie)
        self.data_manager._commit_model_query = MagicMock()

        result = self.data_manager.delete_movie(1)
        self.assertTrue(result["status"])
        self.assertIn("Movie deleted successfully", result["message"])
        self.data_manager._commit_model_query.assert_called_with(mock_movie, operation="delete")

    def test_delete_movie_not_found(self):
        self.data_manager.get_movie_by_id = MagicMock(return_value=None)

        result = self.data_manager.delete_movie(1)
        self.assertFalse(result["status"])
        self.assertIn("Movie not found", result["message"])


if __name__ == "__main__":
    unittest.main()
