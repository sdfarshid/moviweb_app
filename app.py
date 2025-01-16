import secrets

from flask import Flask, render_template, request
import config
from models import init_db, renew_db
from routes.api import api_bp
from routes.movies import movie_bp
from routes.user import user_bp
from services import movie_service
from utils import load_page

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load configuration
app.config.from_object(config)

# Initialize the database
init_db(app)

#register Blueprint
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(api_bp, url_prefix='/api')



@app.route('/', endpoint="home")
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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
