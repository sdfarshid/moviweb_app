import secrets

from flask import Flask,  render_template
import config
from models import init_db, renew_db
from routes.movies import movie_bp
from routes.user import user_bp


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load configuration
app.config.from_object(config)

# Initialize the database
init_db(app)

#register Blueprint
app.register_blueprint(movie_bp, url_prefix="/movies")
app.register_blueprint(user_bp, url_prefix='/users')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
