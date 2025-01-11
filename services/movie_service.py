from typing import Union

from flask import request, flash
from models.user_movie import UserMovie

from api import process_fetching_data_from_API
from exceptions.APIError import FetchingError
from models.movie import Movie
from data_manager import data_manager


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



def proces_add_movie(movie_name: str):
    try:
        movie = is_exist(movie_name)
        if movie is None:
            movie = add_new_movie_with_api(movie_name)
        if movie and movie is not None:
            return movie

        raise ValueError(f"add movie had problem, please try again")

    except (FetchingError, ValueError) as error:
        raise ValueError(f"Have Error in API :{error}")
