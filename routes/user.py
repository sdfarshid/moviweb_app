from flask import Blueprint, render_template, request, redirect, url_for, flash
from services import user_service
from exceptions.UserErrors import UserNotFoundError
from utils import load_page

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/users', endpoint="list_users")
def list_users():
    users = user_service.get_all_users()
    return load_page("users", {"title": "Users List", "users": users})


@user_bp.route('/add_user', methods=["GET", "POST"], endpoint="add_user")
def add_user():
    if request.method == "POST":
        return _handel_add_user_request()
    return load_page("add_user", {"title": "Add User"})


def _handel_add_user_request():
    result = user_service.add_new_user()
    flash_category = "success" if result.get("status") else "error"
    flash(f"{result.get('message')}", f"{flash_category}")
    return redirect(url_for("user_bp.list_users"))


@user_bp.route('/<int:user_id>/movies', endpoint="user_movies")
def user_movies(user_id):
    try:
        user, movies = user_service.user_movies_list(user_id)
        return load_page("user_movies", {"title": f"{user.name}'s Movies", "movies": movies, "user": user})
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("user_bp.list_users"))


@user_bp.route('/<int:user_id>/delete_movie/<int:movie_id>', endpoint="delete_movie")
def delete_movie(user_id, movie_id):
    try:
        user = user_service.get_user(user_id)
        user_service.delete_user_movie(user.id, movie_id)
        flash(f"Movie deleted successfully for {user.name}.", "success")
        return redirect(url_for("user_bp.user_movies", user_id=user.id))
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("user_bp.user_movies"))
