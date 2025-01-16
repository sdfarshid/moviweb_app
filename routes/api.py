from flask import Blueprint, request, jsonify
from services import movie_service, user_service
from exceptions.UserErrors import UserNotFoundError

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/movies', methods=["GET"], endpoint="get_movies")
def get_movies():
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

    return jsonify({
        'movies': [movie.to_dict() for movie in movies],
        'total': total,
        'pages': pages,
        'current_page': current_page
    })


@api_bp.route('/users/add', methods=["POST"], endpoint="add_user")
def add_user():
    user_data = request.get_json()

    if not user_data or 'name' not in user_data:
        return jsonify({"error": "Missing user name"}), 400

    try:
        result = user_service.add_new_user(user_data.get("name"))
        new_user = result.get("data")

        if not new_user:
            return jsonify({"error": "User creation failed"}), 500

        return jsonify(new_user.to_dict()), 201

    except (ValueError, Exception) as error:
        return jsonify({"error": str(error)}), 500


@api_bp.route('/users/list', methods=["GET"], endpoint="list-user")
def list_users():
    users = user_service.get_all_users()
    return jsonify({
        "users": [user.to_dict() for user in users]
    }), 200


@api_bp.route('/users/<int:user_id>/movies', methods=["GET"], endpoint="get_user_movies")
def get_user_movies(user_id):
    try:
        user, movies = user_service.user_movies_list(user_id)
        print(movies)
        return jsonify({
            "user": user.to_dict(),
            "movies": [{"movie": movie["movie"].to_dict(), "note": movie["note"]} for movie in movies]
        }), 200
    except (UserNotFoundError, Exception) as e:
        return jsonify({"error": str(e)}), 404


@api_bp.route('/<int:user_id>/add-user-movie', methods=["POST"], endpoint="add-user-movie")
def add_movie(user_id):
    try:
        user = user_service.get_user(user_id)
        movie_data = request.get_json()
        if not movie_data or 'name' not in movie_data:
            return jsonify({"error": "Missing movie name"}), 400

        movie_name = movie_data['name']
        user_service.add_user_movie(user, movie_name)

        return jsonify({"message": f"The movie '{movie_name}' has been added for {user.name}."}), 201

    except (UserNotFoundError, ValueError, Exception) as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=["PUT"])
def update_movie(user_id, movie_id):
    try:
        user_movie = user_service.get_user_movie_record(user_id, movie_id)
        if not user_movie:
            return jsonify({"error": "User-Movie record not found."}), 400

        movie = user_movie.movie
        user = user_movie.user

        update_request = request.get_json()

        movie_data = {
            "id": movie.id,
            "name": update_request.get("name", movie.name),
            "director": update_request.get("director", movie.director),
            "year": int(update_request.get("year", movie.year)),
            "rating": float(update_request.get("rating", movie.rating))
        }
        movie_service.update_movie(movie_data)
        note = update_request.get("note")
        if note is not None:
            user_service.update_user_movie_note(user.id, movie.id, note)

        return jsonify({
            "user": user.to_dict(),
            "movie": movie_data,
            "note": note if note else movie_data.get("note", ""),
            "message": "Movie updated successfully"}), 200

    except (UserNotFoundError, Exception) as error:
        return jsonify({"error": f"{error}"}), 400


@api_bp.route('/users/<int:user_id>/delete/movie/<int:movie_id>', methods=["DELETE"], endpoint="delete_movie")
def delete_movie(user_id, movie_id):
    try:
        user = user_service.get_user(user_id)
        user_service.delete_user_movie(user.id, movie_id)
        return jsonify({
                    "user": user.to_dict(),
                    "message": "Movie deleted successfully"}
                       ), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


