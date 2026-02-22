import os
from flask import Flask, render_template, request, redirect, url_for, abort
from data_manager import DataManager
from models import db

app = Flask(__name__)

data_mgr = DataManager()


# ------------------ Configuration ------------------

basedir = os.path.abspath(os.path.dirname(__file__))
os.makedirs(os.path.join(basedir, "data"), exist_ok=True)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + os.path.join(basedir, "data", "movi.db")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ------------------ Routes ------------------

@app.route("/")
def index():
    users = data_mgr.get_all_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user_route():
    name = request.form.get("name")
    if not name:
        abort(400, description="User name is required")

    data_mgr.create_user(name)
    return redirect(url_for("index"))


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies_route(user_id):
    user = data_mgr.get_user(user_id)
    if not user:
        abort(404, description="User not found")

    movies = data_mgr.get_movies_by_user(user_id)
    return render_template("movies.html", user=user, movies=movies)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie_route(user_id):
    title = request.form.get("title")
    if not title:
        abort(400, description="Movie title is required")

    data_mgr.add_movie_for_user(user_id, title)
    return redirect(url_for("get_movies_route", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/update",
    methods=["POST"],
)
def update_movie_route(user_id, movie_id):
    new_title = request.form.get("title")
    if new_title:
        data_mgr.update_movie_title(user_id, movie_id, new_title)

    return redirect(url_for("get_movies_route", user_id=user_id))


@app.route(
    "/users/<int:user_id>/movies/<int:movie_id>/delete",
    methods=["POST"],
)
def delete_movie_route(user_id, movie_id):
    data_mgr.delete_movie(user_id, movie_id)
    return redirect(url_for("get_movies_route", user_id=user_id))

# ------------------ Error Handlers ------------------

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template("500.html"), 500

# ------------------ App Start ------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5008)