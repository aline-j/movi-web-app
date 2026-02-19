from models import db, User, Movie
import logging

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

    def update_user(self, user_id, new_name):
        """Update a user's name"""
        try:
            user = db.session.get(User, user_id)
            if not user:
                return None
            user.name = new_name
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating user: {e}")
            return None

    def delete_user(self, user_id):
        """Delete a user"""
        try:
            user = db.session.get(User, user_id)
            if not user:
                return False
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error deleting user: {e}")
            return False

    # ------------------ Movie Methods ------------------

    def create_movie(self, user_id, title, publication_year, cover):
        """Create a new movie for a given user"""
        try:
            user = db.session.get(User, user_id)
            if not user:
                return None
            new_movie = Movie(
                title=title,
                publication_year=publication_year,
                cover=cover,
                user_id=user_id
            )
            db.session.add(new_movie)
            db.session.commit()
            return new_movie
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating movie: {e}")
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
