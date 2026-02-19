import os
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


class DataManger():

    # ------------------ User Methods ------------------

    def create_user(self, name):
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

    def get_all_users(self):
        """Return a list of all users"""
        try:
            return User.query.all()
        except Exception as e:
            logging.error(f"Error fetching all users: {e}")
            return None

    # ------------------ Movie Methods ------------------

    def add_movie_for_user(self, user_id, title):
        """Add a movie for a user using OMDb API"""
        if not OMDB_API_KEY:
            logging.error("OMDB_API_KEY not set in environment variables")
            return None

        try:
            # OMDb API Request
            response = requests.get(
                "http://www.omdbapi.com/",
                params={"t": title, "apikey": OMDB_API_KEY},
                timeout=5
            )
            data = response.json()

            if data.get("Response") == "False":
                logging.info(f"Movie '{title}' not found in OMDb")
                return None

            # Preparing a movie object
            movie_obj = Movie(
                title=data["Title"],
                publication_year=int(data["Year"]),
                cover=data.get("Poster"),
            )

            # Save to database
            return self.create_movie(
                user_id,
                movie_obj.title,
                movie_obj.publication_year,
                movie_obj.cover
            )

        except Exception as e:
            logging.error(
                f"Error adding movie '{title}' for user {user_id}: {e}")
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
