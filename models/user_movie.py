from models import db


class UserMovie(db.Model):
    __tablename__ = 'user_movies'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), primary_key=True)
    added_date = db.Column(db.DateTime, default=db.func.now())
    note = db.Column(db.Text(), nullable=True)  # custom note


    user = db.relationship('User', back_populates='user_movies')
    movie = db.relationship('Movie', back_populates='user_movies')

