from models import db
from models.movie import Movie
from models.user import User
from data_manager.Interface.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):

    def __init__(self):
        self.db = db

    def get_all_users(self) -> list:
        return User.query.all()

    def get_user_by_id(self, user_id: int) -> User:
        return User.query.get(user_id)

    def get_user_movies(self, user_id: int) -> list:
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        return Movie.query.get(movie_id)

    def add_user(self, user_data: dict):
        try:
            user = User(name=user_data["name"])
            self._commit_model_query(user)
            return {"status": True, "message": f"{str(user)} added successfully!"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def add_movie(self, movie_data: dict):
        try:
            movie = Movie(
                name=movie_data["name"],
                director=movie_data["director"],
                year=movie_data["year"],
                rating=movie_data["rating"],
                user_id=movie_data["user_id"]
            )
            self._commit_model_query(movie)
            return {"status": True, "message": f"{str(movie)} added successfully!"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def update_movie(self, movie_data: dict):
        try:
            movie = self.get_movie_by_id(movie_data["id"])
            if movie:
                movie.name = movie_data["name"]
                movie.director = movie_data["director"]
                movie.year = movie_data["year"]
                movie.rating = movie_data["rating"]
                self._commit_model_query(movie)
                return {"status": True, "message": f"{str(movie)} updated successfully!"}
            else:
                return {"status": False, "message": "Movie not found"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def delete_movie(self, movie_id: int):
        try:
            movie = self.get_movie_by_id(movie_id)
            if movie:
                self._commit_model_query(movie, operation="delete")
                return {"status": True, "message": f"Movie deleted successfully!"}
            else:
                return {"status": False, "message": "Movie not found"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def _commit_model_query(self, model, operation="add"):
        try:
            if operation == "add":
                self.db.session.add(model)
            elif operation == "delete":
                self.db.session.delete(model)
            self.db.session.commit()
        except Exception as error:
            self.db.session.rollback()
            raise error
