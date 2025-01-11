from exceptions.UserErrors import UserNotFoundError
from models import db
from models.movie import Movie
from models.user import User
from data_manager.Interface.data_manager_interface import DataManagerInterface
from models.user_movie import UserMovie


class SQLiteDataManager(DataManagerInterface):

    def __init__(self):
        self.db = db

    def get_all_users(self) -> list:
        return User.query.all()

    def get_user_by_id(self, user_id: int) -> User:
        user = User.query.get(user_id)
        if user is None:
            raise UserNotFoundError(f"User not found.")
        return user

    def get_user_movies(self, user_id: int) -> list:
        return Movie.query.filter_by(user_id=user_id).all()

    def get_movie_by_id(self, movie_id: int) -> Movie:
        return Movie.query.get(movie_id)

    def get_movie_by_name(self, movie_name: str) -> Movie:
        return Movie.query.filter_by(name=movie_name).first()

    def add_user(self, user_data: dict):
        try:
            user = User(name=user_data["name"])
            self._commit_model_query(user)
            return {"status": True, "message": f"{str(user)} added successfully!", "data": user}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def assign_user_to_movie(self, user_id: int, movie_id: int):
        try:
            user_movie = UserMovie(user_id=user_id, movie_id=movie_id)
            self._commit_model_query(user_movie)
            return {"status": True, "message": f"{str(user_movie)} added successfully!", "data": user_movie}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def add_movie(self, movie_data: dict):
        try:
            movie = Movie(
                name=movie_data["name"],
                director=movie_data["director"],
                year=movie_data["year"],
                rating=movie_data["rating"],
                poster=movie_data["poster"],
                imdbID=movie_data["imdbID"],
                genre=movie_data["genre"]
            )
            self._commit_model_query(movie)
            return {"status": True, "message": f"{str(movie)} added successfully!", "data": movie}
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

    def delete_user_movie(self, user_id: int, movie_id: int):
        try:
            user_movie = UserMovie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
            if user_movie:
                self._commit_model_query(user_movie, operation="delete")
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
