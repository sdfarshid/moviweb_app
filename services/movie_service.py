from typing import Union

from flask import request, flash

from api import process_fetching_data_from_API
from app import data_manager
from exceptions.APIError import FetchingError
from models.movie import Movie
from models.user_movie import UserMovie


def is_exist(movie_name: str):
    return data_manager.get_movie_by_name(movie_name)


def store_new_movie_data(response: dict) -> dict:
    return data_manager.add_movie({
        "name": response.get("Title", "").lower(),
        "director": response.get("Director", ""),
        "year": response.get("Year", ""),
        "rating": response.get("imdbRating", ""),
        "poster": response.get("Poster", ""),
        "imdbID": response.get("imdbID", ""),
        "genre": response.get("Genre", ""),
    })


def add_new_movie_with_api(movie_name: str) -> Union[Movie, Exception]:
    response = process_fetching_data_from_API(movie_name)
    add_movie_response = store_new_movie_data(response)
    if add_movie_response.get("status") == 'False':
        raise ValueError(add_movie_response.get("message"))

    return add_movie_response.get("data")


def assign_user_to_movie(user_id: int, movie_id: int) -> Union[UserMovie, Exception]:
    response = data_manager.assign_user_to_movie(user_id, movie_id)
    if response.get("status") == 'False':
        raise ValueError(response.get("message"))

    return response.get("data")


def proces_add_movie(user_id: int):
    try:
        movie_name = request.form.get("name")
        movie = is_exist(movie_name)

        if movie is None:
            movie = add_new_movie_with_api(movie_name)


        assign_user_to_movie(user_id, movie.id)

        return True
    except (FetchingError, ValueError) as error:
        flash(f"Have Error in API :{error}", "danger")
        return False
