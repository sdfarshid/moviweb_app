from models import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship("Movie", backref="user", lazy=True)

    def __str__(self):
        return f"User: {self.name}"
