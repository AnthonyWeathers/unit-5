"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")

os.system('createdb ratings')

model.connect_to_db(server.app)

with server.app.app_context():
    model.db.create_all()

    # Load movie data from JSON file
    with open('data/movies.json') as f:
        movie_data = json.loads(f.read())

    # Create movies, store them in list so we can use them
    # to create fake ratings later
    movies_in_db = []
    format = '%Y-%m-%d'

    for movie in movie_data:
        # get the title, overview, and poster_path from the movie
        # dictionary. Then, get the release_date and convert it to a
        # datetime object with datetime.strptime
        title = movie['title']
        overview = movie['overview']
        poster_path = movie['poster_path']
        release_date_str = movie['release_date']
        release_date = datetime.strptime(release_date_str, format)

        # create a movie here and append it to movies_in_db
        movies_in_db.append(crud.create_movie(title=title, overview=overview, release_date=release_date_str, poster_path=poster_path))

    model.db.session.add_all(movies_in_db)
    model.db.session.commit()

    # Create 10 users; each user will make 10 ratings
    for n in range(10):
        email = f"user{n}@test.com"  # Voila! A unique email!
        password = "test"

        user = crud.create_user(email, password)
        model.db.session.add(user)

        for _ in range(10):
            random_movie = choice(movies_in_db)
            score = randint(1, 5)

            rating = crud.create_rating(user, random_movie, score)
            model.db.session.add(rating)

    model.db.session.commit()