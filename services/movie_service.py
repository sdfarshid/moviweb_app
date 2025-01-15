from typing import Union

from flask import request, flash
from sqlalchemy import exists, asc, desc

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


def update_movie(movie_data: dict):
    result = data_manager.update_movie(movie_data)
    if result.get("status") == 'False':
        raise ValueError(result.get("message"))

    return True


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




def get_movie_by_id(movie_id: int):
    return data_manager.get_movie_by_id(movie_id)

def get_movies(sort_by: str = "rating", order: str = "asc", search_query: str = "", page: int = 1, per_page: int = 10):
    """
    Returns movies with pagination, ordered by a specific field (ascending or descending) and optionally filtered by name.
    :param sort_by: The field to sort by (default: "rating").
    :param order: The order of sorting, either "asc" or "desc" (default: "asc").
    :param search_query: The name of the movie to search for (default: "").
    :param page: The page number for pagination (default: 1).
    :param per_page: The number of results per page (default: 10).
    :return: List of movies ordered by the specified field with pagination and optionally filtered by name.
    """
    if order == "asc":
        order_func = asc
    else:
        order_func = desc

    # Filter movies which relative atliest a user
    subquery = exists().where(UserMovie.movie_id == Movie.id)

    # Make query
    query = Movie.query.filter(subquery)

    #Filter by name
    if search_query:
        query = query.filter(Movie.name.ilike(f"%{search_query}%"))

    # add Order by
    query = query.order_by(order_func(getattr(Movie, sort_by)))

    # add Pagination
    query = query.paginate(page=page, per_page=per_page, error_out=False)

    return query.items, query.total, query.pages, query.page