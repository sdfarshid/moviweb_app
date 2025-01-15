from flask import Blueprint, render_template, request, redirect, url_for, flash

from models.movie import Movie
from models.user import User
from services import movie_service
from services import user_service
from exceptions.UserErrors import UserNotFoundError
from utils import load_page




movie_bp = Blueprint('movie_bp', __name__)



@movie_bp.route('/', endpoint="home")
def home():
    MOVIE_PER_PAG = 4
    search_query = request.args.get('search', "")
    sort_by = request.args.get('sort_by', 'rating')  # Default sorting by rating
    sort_order = request.args.get('sort_order', 'asc')  # Default sorting type
    page = request.args.get('page', 1, type=int)  # Current page number
    per_page = request.args.get('per_page', MOVIE_PER_PAG, type=int)  # Number of items per page

    movies, total, pages, current_page = movie_service.get_movies(
        sort_by=sort_by,
        order=sort_order,
        search_query=search_query,
        page=page,
        per_page=per_page
    )
    args = {
        "title": "Home",
        "movies": movies,
        "search_query": search_query,
        "pages": pages,
        "current_page": current_page,
    }
    return load_page("home", args)



@movie_bp.route('/<int:user_id>/add_movie', methods=["GET", "POST"], endpoint="add_movie")
def add_movie(user_id):
    try:
        user = user_service.get_user(user_id)

        if request.method == "POST":
            return _handel_add_user_movie_request(user)

    except (UserNotFoundError, ValueError, Exception) as e:
        flash(str(e), "danger")
        return redirect(url_for("user_bp.list_users"))

    return load_page("add_movie", {"title": f"Add Movie for {user.name}", "user": user})


def _handel_add_user_movie_request(user: User):
    movie_name = request.form.get("name")
    user_service.add_user_movie(user, movie_name)
    flash(f"The movie :  {movie_name} add  for {user.name} ", "success")
    return redirect(url_for("user_bp.user_movies", user_id=user.id))


@movie_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    try:
        user_movie = user_service.get_user_movie_record(user_id, movie_id)
        if not user_movie:
            flash("User-Movie record not found.", "danger")
            return redirect(url_for("user_bp.user_movies", user_id=user_id))

        movie = user_movie.movie
        user = user_movie.user

        if request.method == "POST":
            return _handel_update_user_movie_request(user, movie)
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("user_bp.list_users"))

    args = {
        "title": f"Update Movie for {user_movie.user.name}",
        "user_movie": user_movie,
        "movie": movie,
        "user": user,
    }
    return load_page("update_movie", args)


def _handel_update_user_movie_request(user: User, movie: Movie):
    movie_data = {
        "id": movie.id,
        "name": request.form.get("name"),
        "director": request.form.get("director"),
        "year": int(request.form.get("year")),
        "rating": float(request.form.get("rating")),
    }

    movie_service.update_movie(movie_data)

    note = request.form.get("note")
    user_service.update_user_movie_note(user.id, movie.id, note)

    flash("Movie updated successfully.", "success")
    return redirect(url_for("user_bp.user_movies", user_id=user.id))
