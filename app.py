from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db, Movie
import os

app = Flask(__name__)

data_mgr = DataManager()

os.makedirs('data', exist_ok=True)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "sqlite:///" + os.path.join(basedir, "data", "movi.db")
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route('/')
def index():
    users = data_mgr.get_all_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user_route():
    name = request.form.get('name')

    if not name:
        abort(400, description="User name is required")

    try:
        data_mgr.create_user(name)
        return redirect(url_for('index'))
    except Exception as e:
        abort(500, description=f"Error fetching movies: {e}")


@app.route('/users', methods=['GET'])
def get_users_route():
    users = data_mgr.get_all_users()
    return str(users)


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def get_movies_route(user_id):
    try:
        user = data_mgr.get_user(user_id)
        if not user:
            abort(404, description="User not found")

        movies = data_mgr.get_movies_by_user(user_id)
        return render_template('movies.html', user=user, movies=movies)

    except Exception as e:
        abort(500, description=f"Error fetching movies: {e}")


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_route(user_id):
    title = request.form.get('title')

    if not title:
        abort(400, description="Movie title is required")

    try:
        data_mgr.add_movie_for_user(user_id, title)
        return redirect(url_for('get_movies_route', user_id=user_id))

    except Exception as e:
        abort(500, description=str(e))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/update",
    methods=["POST"]
)
def update_movie_route(user_id, movie_id):
    new_title = request.form.get("title")

    if new_title:
        data_mgr.update_movie_title(user_id, movie_id, new_title)

    return redirect(url_for("get_movies_route", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/delete",
    methods=["POST"]
)
def delete_movie_route(user_id, movie_id):
    data_mgr.delete_movie(user_id, movie_id)
    return redirect(url_for("get_movies_route", user_id=user_id))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5008)
