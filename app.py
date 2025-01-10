import secrets

from flask import Flask, request, redirect, url_for, render_template, flash
import config
from exceptions.UserErrors import UserNotFoundError
from models import init_db, renew_db
from data_manager.sqlite_data_manager import SQLiteDataManager
import services.movie_service

app = Flask(__name__)

app.config.from_object(config)
app.secret_key = secrets.token_hex(16)


init_db(app)

data_manager = SQLiteDataManager()


def load_page(template_name: str, args=None):
    if args is None:
        args = {}
    return render_template(f'{template_name}.html', **args)


@app.route('/')
def home():
    return load_page("home", {"title": "Home"})


@app.route('/users', endpoint="list_users")
def list_users():
    users = data_manager.get_all_users()
    return load_page("users", {"title": "Users List", "users": users})

@app.route('/add_user', methods=["GET", "POST"], endpoint="add_user")
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        result = data_manager.add_user({"name": name})
        flash_category = "success" if result.get("status") else "error"
        flash(f"{result.get("message")}", f"{flash_category}")
        return redirect(url_for("list_users"))
    return load_page("add_user", {"title": "Add User"})


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        user = data_manager.get_user_by_id(user_id)
        movies = user.movies
        return load_page("user_movies", {"title": f"{user.name}'s Movies", "movies": movies, "user": user})
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("list_users"))

@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    try:
        user = data_manager.get_user_by_id(user_id)
        if user is None:
            flash("User not found", "error")
            return redirect(url_for("list_users"))

        if request.method == "POST":
            result = services.movie_service.proces_add_movie(user_id)
            if result:
                flash(f"The movie :  {request.form.get("name")} add  for {user.name} ", "success")

            return redirect(url_for("user_movies", user_id=user_id))
        return load_page("add_movie", {"title": f"Add Movie for {user.name}", "user": user})

    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("list_users"))

@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    movie = data_manager.get_movie_by_id(movie_id)
    if request.method == "POST":
        movie_data = {
            "id": movie_id,
            "name": request.form.get("name"),
            "director": request.form.get("director"),
            "year": int(request.form.get("year")),
            "rating": float(request.form.get("rating")),
            "user_id": user_id
        }
        data_manager.update_movie(movie_data)
        return redirect(url_for("user_movies", user_id=user_id))
    return load_page("update_movie", {"title": "Update Movie", "movie": movie})


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(movie_id)
    return redirect(url_for("user_movies", user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
