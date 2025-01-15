import secrets

from flask import Flask, request, redirect, url_for, render_template, flash
import config
from exceptions.UserErrors import UserNotFoundError
from models import init_db, renew_db
from models.movie import Movie
from models.user import User
from routes.movies import movie_bp
from services import user_service, movie_service

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load configuration
app.config.from_object(config)

# Initialize the database
init_db(app)




def load_page(template_name: str, args=None):
    if args is None:
        args = {}
    return render_template(f'{template_name}.html', **args)


@app.route('/')
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


@app.route('/users', endpoint="list_users")
def list_users():
    users = user_service.get_all_users()
    return load_page("users", {"title": "Users List", "users": users})


@app.route('/add_user', methods=["GET", "POST"], endpoint="add_user")
def add_user():
    if request.method == "POST":
        return _handel_add_user_request()
    return load_page("add_user", {"title": "Add User"})


def _handel_add_user_request():
    result = user_service.add_new_user()
    flash_category = "success" if result.get("status") else "error"
    flash(f"{result.get("message")}", f"{flash_category}")
    return redirect(url_for("list_users"))


@app.route('/users/<int:user_id>')
def user_movies(user_id):
    try:
        (user, movies) = user_service.user_movies_list(user_id)
        return load_page("user_movies", {"title": f"{user.name}'s Movies", "movies": movies, "user": user})
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("list_users"))


@app.route('/users/<int:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    try:
        user = user_service.get_user(user_id)

        if request.method == "POST":
            return _handel_add_user_movie_request(user)

    except (UserNotFoundError, ValueError, Exception) as e:
        flash(str(e), "danger")
        return redirect(url_for("list_users"))

    return load_page("add_movie", {"title": f"Add Movie for {user.name}", "user": user})


def _handel_add_user_movie_request(user: User):
    movie_name = request.form.get("name")
    user_service.add_user_movie(user, movie_name)
    flash(f"The movie :  {movie_name} add  for {user.name} ", "success")
    return redirect(url_for("user_movies", user_id=user.id))


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    try:
        user = user_service.get_user(user_id)
        user_service.delete_user_movie(user.id, movie_id)
        flash(f"Movie deleted successfully for {user.name}.", "success")
        return redirect(url_for("user_movies", user_id=user.id))
    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("user_movies"))


@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    try:
        user_movie = user_service.get_user_movie_record(user_id, movie_id)
        if not user_movie:
            flash("User-Movie record not found.", "danger")
            return redirect(url_for("user_movies", user_id=user_id))

        movie = user_movie.movie
        user = user_movie.user

        if request.method == "POST":
            return _handel_update_user_movie_request(user, movie)

    except UserNotFoundError as e:
        flash(str(e), "danger")
        return redirect(url_for("list_users"))


    return load_page("update_movie", {
            "title": f"Update Movie for {user_movie.user.name}",
            "user_movie": user_movie,
            "movie": movie,
            "user": user,
        })


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
    return redirect(url_for("user_movies", user_id=user.id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
