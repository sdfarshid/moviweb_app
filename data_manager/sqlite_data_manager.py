from models import db
from models.movie import Movie
from models.user import User
from data_manager.Interface.data_manager_interface import DataManagerInterface


class SQLiteDataManager(DataManagerInterface):

    def __init__(self):
        self.db = db

    def get_all_users(self) -> list:
        return User.query.all()

    def get_user_movies(self, user_id):
        return Movie.query.filter_by(user_id=user_id).all()

    def add_user(self, user: User):
        try:
            self._commit_model_query(user)
            return {"status": True, "message": f"{str(user)} added successfully!"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def add_movie(self, movie: Movie):
        try:
            self._commit_model_query(movie)
            return {"status": True, "message": f"{str(movie)} added successfully!"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def update_movie(self, movie: Movie):
        try:
            self._commit_model_query(movie)
            return {"status": True, "message": f"{str(movie)} added successfully!"}
        except Exception as error:
            return {"status": False, "message": f"Error: {str(error)}"}

    def delete_movie(self, movie_id: int):
        movie = Movie.query.get(movie_id)
        if movie:
            try:
                self._commit_model_query(movie, operation="delete")
                return {"status": True, "message": f"{str(movie)} added successfully!"}
            except Exception as error:
                return {"status": False, "message": f"Error: {str(error)}"}
        else:
            raise ValueError("Movie not found")

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
