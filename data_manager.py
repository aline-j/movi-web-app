import os
from lib2to3.main import diff_texts

import requests
from models import db, User, Movie
import logging

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    filename='app.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def create_user(name):
    """Create a new user"""
    try:
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error creating user: {e}")
        return None


class DataManager():

    # ------------------ User Methods ------------------

    def get_all_users(self):
        """Return a list of all users"""
        try:
            return User.query.all()
        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
            return None

    def create_user(self, name):
        """Add a new user if it doesn't exist"""
        try:
            return create_user(name)
        except Exception as e:
            logging.error(f"Error create new user: {e}")
            return None

    def get_user(self, user_id):
        """Return a user by ID"""
        try:
            return User.query.get(user_id)
        except Exception as e:
            logging.error(f"Error fetching user {user_id}: {e}")


    # ------------------ Movie Methods ------------------

    def add_movie_for_user(self, user_id, title):
        """Add a movie for a user using OMDb API"""
        if not OMDB_API_KEY:
            logging.error("OMDB_API_KEY not set")
            return None

        try:
            response = requests.get(
                "http://www.omdbapi.com/",
                params={"t": title, "apikey": OMDB_API_KEY},
                timeout=5
            )
            data = response.json()

            if data.get("Response") == "False":
                logging.info(f"Movie '{title}' not found")
                return None

            movie = Movie(
                title=data["Title"],
                publication_year=int(data["Year"]),
                director=data.get("Director"),
                cover=data.get("Poster"),
                user_id=user_id
            )

            db.session.add(movie)
            db.session.commit()
            return movie

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding movie: {e}")
            return None

    def get_movies_by_user(self, user_id):
        """Return all movies for a given user"""
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except Exception as e:
            logging.error(f"Error fetching movies for user {user_id}: {e}")
            return None

    def update_movie_title(self, user_id, movie_id, new_title):
        """Update the title of a movie for a given user"""
        try:
            movie = db.session.get(Movie, movie_id)
            if not movie or movie.user_id != user_id:
                return None
            movie.title = new_title
            db.session.commit()
            return movie
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating movie title: {e}")
            return None

    def delete_movie(self, user_id, movie_id):
        """Delete a movie if it belongs to the user"""
        try:
            movie = db.session.get(Movie, movie_id)
            if not movie or movie.user_id != user_id:
                return False
            db.session.delete(movie)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting movie: {e}")
            return False

