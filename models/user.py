from models import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    user_movies = db.relationship('UserMovie', back_populates='user')

    @property
    def movies(self):
        return [user_movie.movie for user_movie in self.user_movies]


    @property
    def movie_count(self):
        return len(self.user_movies)



    def __str__(self):
        return f"User: {self.name}"


