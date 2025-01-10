from models import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    name = db.Column(db.String(200), nullable=False)  # Movie name
    director = db.Column(db.String(100), nullable=False)  # Director's name
    year = db.Column(db.Integer, nullable=False)  # Year of release
    imdbID = db.Column(db.String(100), nullable=True)  # IMDb ID as text
    genre = db.Column(db.Text(), nullable=True)  # Gerne  as text
    rating = db.Column(db.Float, nullable=False)  # Movie rating (e.g., 1.0 to 10.0)
    poster = db.Column(db.Text(), nullable=True)  # poster' link

    # Many To Many via UserMovie
    user_movies = db.relationship('UserMovie', back_populates='movie')

def __str__(self):
    return f"movie: {self.title}"
