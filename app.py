import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import workouts
import re


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

@app.route("/")
def index():
    all_workouts = workouts.get_workouts()
    return render_template("index.html", workouts=all_workouts)

@app.route("/find_workout")
def find_workout():
    query = request.args.get("query")
    if query:
        results = workouts.find_workouts(query)
    else:
        query = ""
        results = []
    return render_template("find_workout.html", query=query, results=results)

@app.route("/workout/<int:workout_id>")
def show_workout(workout_id):
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)
    return render_template("show_workout.html", workout=workout)

@app.route("/new_workout")
def new_workout():
    require_login()
    return render_template("new_workout.html")

@app.route("/create_workout", methods=["POST"])
def create_workout():
    require_login()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    duration = request.form["duration"]
    if not re.search("^[1-9][0-9]{0,2}$", duration):
        abort(403)
    intensity = request.form["intensity"]
    user_id = session["user_id"]

    workouts.add_workout(title, description, duration, intensity, user_id)

    return redirect("/")

@app.route("/edit_workout/<int:workout_id>")
def edit_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)
    return render_template("edit_workout.html", workout=workout)

@app.route("/update_workout", methods=["POST"])
def update_workout():
    require_login()
    workout_id = request.form["workout_id"]
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    duration = request.form["duration"]
    if not re.search("^[1-9][0-9]{0,2}$", duration):
        abort(403)
    intensity = request.form["intensity"]

    workouts.update_workout(workout_id, title, description, duration, intensity)

    return redirect("/workout/" + str(workout_id))

@app.route("/remove_workout/<int:workout_id>", methods=["GET", "POST"])
def remove_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("remove_workout.html", workout=workout)

    if request.method == "POST":
        if "remove" in request.form:
            workouts.remove_workout(workout_id)
            return redirect("/")
        else:
            return redirect("/workout/" + str(workout_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["user_id"] = user_id
            session["username"] = username
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
