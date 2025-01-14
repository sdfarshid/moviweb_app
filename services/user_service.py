from typing import Union

from flask import request, flash

from exceptions.UserErrors import UserNotFoundError
from models.user import User
from models.user_movie import UserMovie
from services.movie_service import proces_add_movie

from data_manager import data_manager


def get_user(user_id: int):
    try:
        return data_manager.get_user_by_id(user_id)
    except UserNotFoundError:
        raise UserNotFoundError("User not found.")


def user_movies_list(user_id: int):
    user = get_user(user_id)
    movies = user.movies
    return user, movies




def add_user_movie(user: User, movie_name: str):
    try:
        user_id = user.id
        new_movie = proces_add_movie(movie_name)
        assign_user_to_movie(user_id, new_movie.id)
        return True
    except ValueError as erro:
        flash(f"{erro}", "danger")
        raise ValueError(erro)


def assign_user_to_movie(user_id: int, movie_id: int) -> Union[UserMovie, Exception]:
    response = data_manager.assign_user_to_movie(user_id, movie_id)
    if response.get("status") == 'False':
        raise ValueError(response.get("message"))

    return response.get("data")


def delete_user_movie(user_id: int, movie_id: int):
    result = data_manager.delete_user_movie(user_id, movie_id)
    if result.get("status") == 'False':
        raise ValueError(result.get("message"))

    return True



def get_all_users():
    return data_manager.get_all_users()


def add_new_user():
    name = request.form.get("name")
    return data_manager.add_user({"name": name})


def get_user_movie_record(user_id: int, movie_id: int):
    return data_manager.get_user_movie_record(user_id, movie_id)



def update_user_movie_note(user_id: int, movie_id: int, note: str):
    result = data_manager.update_user_movie_note(user_id, movie_id, note)
    if result.get("status") == 'False':
        raise ValueError(result.get("message"))
    return True
