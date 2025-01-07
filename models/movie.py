from models import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique identifier
    name = db.Column(db.String(200), nullable=False)  # Movie name
    director = db.Column(db.String(100), nullable=False)  # Director's name
    year = db.Column(db.Integer, nullable=False)  # Year of release
    rating = db.Column(db.Float, nullable=False)  # Movie rating (e.g., 1.0 to 10.0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, director, year, rating, user_id):
        self.name = name
        self.director = director
        self.year = year
        self.rating = rating
        self.user_id = user_id


def __str__(self):
    return f"movie: {self.title}"
