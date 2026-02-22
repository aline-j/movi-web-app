import os
from dotenv import load_dotenv
import requests
import logging
from models import db, User, Movie


load_dotenv()

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

if not OMDB_API_KEY:
    raise RuntimeError(
        "OMDB_API_KEY is not set."
        "Please configure the environment variable with your OMDb API key"
        "(see README)."
    )

logger = logging.getLogger(__name__)


class DataManager:
    # ------------------ User Methods ------------------

    def get_user(self, user_id):
        """Return a user by ID"""
        try:
            return db.session.get(User, user_id)
        except Exception:
            logger.exception(f"Error fetching user {user_id}")
            return None

    def get_all_users(self):
        """Return a list of all users"""
        try:
            return User.query.all()
        except Exception as e:
            logger.exception("Error fetching all users")
            return []

    def create_user(self, name):
        """Create a new user"""
        try:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            logger.exception("Error creating user")
            return None

    # ------------------ Movie Methods ------------------

    def add_movie_for_user(self, user_id, title):
        """Add a movie for a user using OMDb API"""
        if not OMDB_API_KEY:
            logger.error("OMDB_API_KEY not set")
            return None

        user = get_user(user_id)
        if not user:
            logger.warning(f"User {user_id} not found")
            return None

        try:
            response = requests.get(
                "https://www.omdbapi.com/",
                params={"t": title, "apikey": OMDB_API_KEY},
                timeout=5
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "False":
                logger.info(f"Movie '{title}' not found")
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

        except Exception:
            db.session.rollback()
            logger.exception("Error adding movie")
            return None

    def get_movies_by_user(self, user_id):
        """Return all movies for a given user"""
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except Exception:
            logger.exception(f"Error fetching movies for user {user_id}")
            return []

    def update_movie_title(self, user_id, movie_id, new_title):
        """Update the title of a movie for a given user"""
        try:
            movie = db.session.get(Movie, movie_id)

            if not movie or movie.user_id != user_id:
                return None

            movie.title = new_title
            db.session.commit()
            return movie

        except Exception:
            db.session.rollback()
            logger.exception("Error updating movie title")
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

        except Exception:
            db.session.rollback()
            logger.exception("Error deleting movie")
            return False
