"""CRUD operations."""

from model import db, User, Movie, Rating, connect_to_db

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    """Return all users."""
    return User.query.all()

def get_user_by_id(id):
    """Return a user's profile."""
    return User.query.get(id)

def get_user_by_email(email):
    """Return a user's profile."""
    return User.query.filter(User.email == email).first()

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""

    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)

    return movie

def get_movies():
    """Return all movies."""
    return Movie.query.all()

def get_movie_by_id(id):
    """Return a movie's details."""
    return Movie.query.get(id)

def create_rating(user, movie, score):
    """Create and return a new rating."""

    rating = Rating(user=user, movie=movie, score=score)

    return rating

def get_rating_by_att(user_id, movie_id):
    """Return a movie's details."""
    return Rating.query.filter(Rating.user_id == user_id, Rating.movie_id == movie_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)