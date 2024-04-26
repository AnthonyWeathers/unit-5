"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,
                    redirect, jsonify)
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/movies')
def all_movies():
    """View all movies."""

    movies = crud.get_movies()

    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def get_movie(movie_id):
    """View a movie's details."""
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session['primary_key'])

    return render_template('movie_details.html', movie=movie, user_id=user.user_id)

@app.route('/users')
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template('all_users.html', users=users)

@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    if crud.get_user_by_email(email):
        flash(f"This email is already in use, please use another.")
        return redirect("/")

    user = crud.create_user(email, password)
    db.session.add(user)
    db.session.commit()
    flash(f"Your account was successfully created and you can now login.")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    """A user logs in."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user and user.password == password:
        flash(f"Successfully logged in.")
        session["primary_key"] = user.user_id
        return redirect("/")

    flash(f"Either email or password was incorrect, please try again.")
    return redirect("/")

@app.route('/users/<user_id>')
def get_user(user_id):
    """View a user's profile."""

    user = crud.get_user_by_id(user_id)

    return render_template('user_profile.html', user=user)

@app.route('/rate/<movie_id>', methods=["POST"])
def rate(movie_id):
    """View a user's profile."""
    session["movie_key"] = movie_id

    user = crud.get_user_by_id(session['primary_key'])
    movie = crud.get_movie_by_id(movie_id)

    if crud.get_rating_by_att(user_id=user.user_id, movie_id=movie_id):
        flash(f"Already made a rating for this movie.")
    else:
        score = int(request.form.get("rating"))

        rating = crud.create_rating(user=user, movie=movie, score=score)
        db.session.add(rating)
        db.session.commit()

    return render_template('movie_details.html', movie=movie, user_id=user.user_id)

@app.route('/update_rating', methods=['POST'])
def update_rating():
    # Get data from the AJAX request
    data = request.json  # Assuming data is sent as JSON
    new_rating = data.get('new_rating')

    user = crud.get_user_by_id(session['primary_key'])
    movie = crud.get_movie_by_id(session['movie_key'])

    # Update the rating in the database
    rating = crud.get_rating_by_att(user_id=user.user_id, movie_id=movie.movie_id)
    if rating:
        rating.score = new_rating
        db.session.commit()

        # grab only the score attribute from the rating object returned from the database
        rating = {
            'score': rating.score
        }
        return jsonify(rating)
    else:
        return jsonify({'error': 'Rating not found'}), 404

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
