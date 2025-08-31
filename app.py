import re
import secrets
import sqlite3

from flask import Flask
from flask import abort, flash, redirect, render_template, request, session

import markupsafe
import config
import db
import workouts
import users


app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if "csrf_token" not in request.form:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
def index():
    all_workouts = workouts.get_workouts()
    return render_template("index.html", workouts=all_workouts)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    workouts = users.get_workouts(user_id)
    return render_template("show_user.html", user=user, workouts=workouts)

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
    classes = workouts.get_classes(workout_id)
    evaluations = workouts.get_evaluations(workout_id)
    return render_template("show_workout.html", workout=workout,
                           classes=classes, evaluations=evaluations)

@app.route("/new_workout")
def new_workout():
    require_login()
    classes = workouts.get_all_classes()
    return render_template("new_workout.html", classes=classes)

@app.route("/create_workout", methods=["POST"])
def create_workout():
    require_login()
    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    description = request.form["description"]
    if not description or len(description) > 1000:
        abort(403)
    duration = request.form["duration"]
    if not re.search("^[1-9][0-9]{0,2}$", duration):
        abort(403)
    user_id = session["user_id"]

    all_classes = workouts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    workout_id = workouts.add_workout(title, description, duration, user_id, classes)
    return redirect("/workout/" + str(workout_id))

@app.route("/create_evaluation", methods=["POST"])
def create_evaluation():
    require_login()
    check_csrf()

    workout_id = request.form.get('workout_id')
    user_id = session["user_id"]
    evaluation = request.form["evaluation"]
    if not evaluation or len(evaluation) > 1000:
        abort(403)

    workouts.add_evaluation(workout_id, user_id, evaluation)

    return redirect("/workout/" + str(workout_id))

@app.route("/edit_workout/<int:workout_id>")
def edit_workout(workout_id):
    require_login()
    workout = workouts.get_workout(workout_id)
    if not workout:
        abort(404)
    if workout["user_id"] != session["user_id"]:
        abort(403)

    all_classes = workouts.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in workouts.get_classes(workout_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_workout.html", workout=workout, classes=classes,
    all_classes=all_classes)

@app.route("/update_workout", methods=["POST"])
def update_workout():
    require_login()
    check_csrf()

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

    all_classes = workouts.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            if parts[0] not in all_classes:
                abort(403)
            if parts[1] not in all_classes[parts[0]]:
                abort(403)
            classes.append((parts[0], parts[1]))

    workout_id = workouts.update_workout(workout_id, title, description, duration, classes)

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
        check_csrf()
        if "remove" in request.form:
            workouts.remove_workout(workout_id)
            return redirect("/")
    return redirect("/workout/" + str(workout_id))


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1 or not password2:
        flash("VIRHE: käyttäjätunnus ja salasana ovat pakollisia")
        return redirect("/register")

    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    if len(password1) < 8:
        flash("VIRHE: salasanan on oltava vähintään 8 merkkiä")
        return redirect("/register")

    try:
        users.create_user(username, password1)
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/login")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")
